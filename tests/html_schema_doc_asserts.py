from typing import List

from bs4 import BeautifulSoup


def assert_soup_results_text(soup: BeautifulSoup, class_name: str, texts: List[str]) -> None:
    """Assert that all the HTML elements with the provided class found in the schema has the supplied text

    There must be exactly as many elements as the length of the supplied values and they must be in the same order
    """
    elements = soup.find_all(class_=class_name)

    assert len(elements) == len(texts)

    for i, element in enumerate(elements):
        assert element.text.strip() == texts[i]


def assert_property_names(soup: BeautifulSoup, property_names: List[str]) -> None:
    assert_soup_results_text(soup, "property-name", property_names)


def assert_title(soup: BeautifulSoup, title: str) -> None:
    """Assert the result file contains the provided title"""
    assert soup.head.title.string == title
    assert soup.body.h1.string == title


def assert_descriptions(soup: BeautifulSoup, descriptions: List[str]) -> None:
    """Assert the result file contains exactly the provided descriptions in the same order"""
    assert_soup_results_text(soup, "description", descriptions)


def assert_types(soup: BeautifulSoup, type_names: List[str]) -> None:
    assert_soup_results_text(soup, "value-type", [f"Type: {type_name}" for type_name in type_names])


def assert_const(soup: BeautifulSoup, const_values: List[str]) -> None:
    assert_soup_results_text(soup, "const-value", [f'Specific value: "{const_value}"' for const_value in const_values])


def assert_numeric_restrictions(soup: BeautifulSoup, restrictions: List[str]) -> None:
    assert_soup_results_text(soup, "numeric-restriction", restrictions)


def assert_one_of_options(soup: BeautifulSoup, nb_options: int) -> None:
    assert_soup_results_text(soup, "oneOf-option", [f"Option {str(i + 1)}" for i in range(nb_options)])


def assert_default_values(soup: BeautifulSoup, default_values: List[str]) -> None:
    assert_soup_results_text(soup, "default-value", [f"Default: {default_value}" for default_value in default_values])


def assert_badges(soup: BeautifulSoup, badge_class_name: str, expected_values: List[bool]) -> None:
    """Assert that the badge with the given class name is either present or not for all properties"""
    property_cards = soup.find_all(class_="property-name-button")
    assert len(property_cards) == len(expected_values)

    for i, property_card in enumerate(property_cards):
        assert (property_card.find(class_=f"{badge_class_name}-property") is not None) == expected_values[i]


def assert_deprecated(soup: BeautifulSoup, is_deprecated_properties: List[bool]) -> None:
    assert_badges(soup, "deprecated", is_deprecated_properties)


def assert_required(soup: BeautifulSoup, is_required_properties: List[bool]) -> None:
    assert_badges(soup, "required", is_required_properties)


def assert_basic_case(soup: BeautifulSoup) -> None:
    """Assert the rendered result of the basic test case"""
    assert_property_names(soup, ["firstName", "lastName", "age"])
    assert_descriptions(
        soup,
        [
            "The person's first name.",
            "The person's last name.",
            "Age in years which must be equal to or greater than zero.",
        ],
    )
    assert_title(soup, "Person")
    assert_numeric_restrictions(soup, ["Value must be greater or equal to 0"])
    assert_required(soup, [False] * 3)
