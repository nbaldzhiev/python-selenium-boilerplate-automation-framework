"""The module contains an abstraction implementation of a multi select dropdown type of element."""
from __future__ import annotations

import logging
from typing import List, Optional, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from elements.dropdowns.base_dropdown import BaseDropdown, BaseExpandedDropdown
from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class MultiSelectExpandedDropdown(BaseExpandedDropdown):
    """This class inherits the base expanded dropdown to implement the additional components of
    a multi-select expanded dropdown."""

    DEFAULT_APPLY_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[aria-label*="Apply"]')
    DEFAULT_CANCEL_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[aria-label*="Cancel"]')

    def __init__(
        self,
        locator: Tuple[By, str],
        options_locator: Tuple[By, str],
        apply_button_locator: Tuple[By, str] = DEFAULT_APPLY_BUTTON_LOCATOR,
        cancel_button_locator: Tuple[By, str] = DEFAULT_CANCEL_BUTTON_LOCATOR,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        web_element: Optional[WebElement] = None,
    ):
        # pylint: disable=duplicate-code
        super().__init__(
            parent=parent,
            locator=locator,
            options_locator=options_locator,
            web_element=web_element,
        )
        self.apply_button = BaseWebElement(parent=self, locator=apply_button_locator)
        self.cancel_button = BaseWebElement(parent=self, locator=cancel_button_locator)

    def apply(self):
        """Applies the options selected in the expanded dropdown by clicking on the Apply button."""
        self.apply_button.click()

    def cancel(self):
        """Closes the expanded dropdown by clicking on the Cancel button."""
        self.cancel_button.click()


class MultiSelectDropdown(BaseDropdown):
    """This class implements an abstraction of a multi-select dropdown."""

    # Default locators to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for dropdown elements in your project
    DEFAULT_LOCATOR = (By.CSS_SELECTOR, 'button[class*="dropdown"]')
    DEFAULT_EXPANDED_LOCATOR = (
        By.CSS_SELECTOR,
        'div[class*="hoverable-content--visible"]',
    )
    DEFAULT_EXPANDED_OPTIONS_LOCATOR = (
        By.CSS_SELECTOR,
        'li[class="collection-values-item"] ',
    )

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Tuple[By, str] = DEFAULT_LOCATOR,
        web_element: Optional[WebElement] = None,
        expanded_locator: Tuple[By, str] = DEFAULT_EXPANDED_LOCATOR,
        expanded_options_loc: Tuple[By, str] = DEFAULT_EXPANDED_OPTIONS_LOCATOR,
    ):
        super().__init__(
            parent=parent,
            locator=locator,
            expanded_locator=expanded_locator,
            expanded_options_loc=expanded_options_loc,
            web_element=web_element,
        )

    @property
    def expanded(self) -> MultiSelectExpandedDropdown:
        """The expanded container of the dropdown.

        Returns
        -------
        MultiSelectExpandedDropdown
        """
        from settings import GLOBAL_DRIVER

        return MultiSelectExpandedDropdown(
            parent=GLOBAL_DRIVER,
            locator=self._expanded_locator,
            options_locator=self._expanded_options_locator,
        )

    def select_options(self, options_values: List[Union[str, int]]):
        """Selects options from the dropdown if they are not already set.

        Parameters
        ----------
        options_values : List[Union[str, int]]
            The option to select.
        """
        for option in options_values:
            # Do nothing if the option is already selected. This depends on the dropdown
            # implementation. The implementation here is of an example
            # where the selected options become a comma-separated string value of the dropdown
            if option.lower() in self.text.lower().split(", "):
                return

            self.expand_dropdown()
            filtered = list(
                filter(
                    lambda opt: option.lower() in opt.text.lower(),
                    self.expanded.options_as_web_elements,
                )
            )
            if not filtered:
                raise UserWarning(
                    f"The option {option} was not found in dropdown with locator: {self.locator}"
                )

            filtered[0].click()
            logging.info(
                "Selected option: %s, for multi-select dropdown with locator: %s",
                option,
                self.locator,
            )

        self.expanded.apply()
        logging.info(
            "Applied the options: %s, selected for the multi-select dropdown with locator: %s",
            options_values,
            self.locator,
        )
