"""The module contains an abstraction implementation of a single select dropdown type of element."""
from __future__ import annotations

import logging
from typing import Optional, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from elements.dropdowns.base_dropdown import BaseDropdown, BaseExpandedDropdown
from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class SingleSelectExpandedDropdown(BaseExpandedDropdown):
    """This class inherits the base expanded dropdown to implement the additional components of
    a single-select expanded dropdown."""

    def __init__(
        self,
        locator: Tuple[By, str],
        options_locator: Tuple[By, str],
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(
            parent=parent,
            locator=locator,
            options_locator=options_locator,
            web_element=web_element,
        )


class SingleSelectDropdown(BaseDropdown):
    """This class implements an abstraction of a single-select dropdown."""

    # A default CSS selector to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for dropdown elements in your project
    DEFAULT_LOCATOR = (By.CSS_SELECTOR, 'button[class*="dropdown"]')
    DEFAULT_EXPANDED_LOCATOR = (
        By.CSS_SELECTOR,
        'div[class*="dropdown__content--is-open"]',
    )
    DEFAULT_EXPANDED_OPTIONS_LOCATOR = (By.CSS_SELECTOR, 'li[class*="dropdown-item"]')

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Tuple[By, str] = DEFAULT_LOCATOR,
        web_element: Optional[WebElement] = None,
        expanded_locator: Tuple[By, str] = DEFAULT_EXPANDED_LOCATOR,
        expanded_options_loc: Tuple[By, str] = DEFAULT_EXPANDED_OPTIONS_LOCATOR,
    ):
        # pylint: disable=duplicate-code
        super().__init__(
            parent=parent,
            locator=locator,
            expanded_locator=expanded_locator,
            expanded_options_loc=expanded_options_loc,
            web_element=web_element,
        )

    @property
    def expanded(self) -> SingleSelectExpandedDropdown:
        """The expanded container of the dropdown.

        Returns
        -------
        SingleSelectExpandedDropdown
        """
        from settings import GLOBAL_DRIVER

        return SingleSelectExpandedDropdown(
            parent=GLOBAL_DRIVER,
            locator=self._expanded_locator,
            options_locator=self._expanded_options_locator,
        )

    def select_option(self, option_value: Union[str, int]):
        """Selects an option from the dropdown if it's not already set.

        Parameters
        ----------
        option_value : Union[str, int]
            The option to select.
        """
        # Do nothing if the currently selected option is the one received as an argument
        if self.text.lower() == option_value.lower():
            return

        option = list(
            filter(
                lambda opt: opt.text.lower() == option_value.lower(),
                self.expand_dropdown().options_as_web_elements,
            )
        )
        if not len(option):
            raise UserWarning(f"The option with value: {option_value}, was not found!")

        option[0].click()
        logging.info(
            "Selected option: %s, of dropdown with locator: %s.",
            option_value,
            self.locator,
        )
