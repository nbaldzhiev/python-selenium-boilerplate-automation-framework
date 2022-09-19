"""This module contains an implementation of a input type of element in a given UI."""
from __future__ import annotations

import logging
from typing import Optional, Tuple, Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from settings import GLOBAL_DRIVER, LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class Input(BaseWebElement):
    """This class implements an abstraction of an input type of element in a UI."""

    # A default CSS selector to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for input elements in your project
    DEFAULT_CSS_SELECTOR = 'input[id="inlineUserEmail"]'

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Optional[Tuple[By, str]] = None,
        web_element: Optional[WebElement] = None,
    ):
        if not (locator or web_element):
            super().__init__(
                parent=parent,
                locator=(By.CSS_SELECTOR, type(self).DEFAULT_CSS_SELECTOR),
            )
        else:
            super().__init__(parent=parent, locator=locator, web_element=web_element)

    def clear_input(self) -> Input:
        """Clears the input of any characters currently typed in. The method clears the input
        value by doing a triple click to select all text and then clicking the backspace button.
        This is done because WebElement's clear() method does not work in some situations.

        Returns
        -------
        Input
            Returns the instance itself to allow for a fluent interface.
        """
        ActionChains(GLOBAL_DRIVER).double_click(
            on_element=self.find_element()
        ).click().perform()
        self.web_element.send_keys(Keys.BACK_SPACE)
        logging.info(
            "Cleared the input of Input element with locator: %s", self.locator
        )
        return self

    def enter_value(self, value: Union[str, int], clear_first: bool = True) -> Input:
        """Types in given value into the input.

        Parameters
        ----------
        value : Union[str, int]
            The value, i.e. characters, to type in the input.
        clear_first : bool
            Controls whether the input would first be cleared before typing in it. Defaults to True.

        Returns
        -------
        Input
            Returns the instance itself to allow for a fluent interface.
        """
        clear_first and self.clear_input()
        self.find_element().send_keys(value)
        logging.info(
            "Entered the value: %s to the Input element with locator: %s",
            value,
            self.locator,
        )
        return self

    @property
    def current_input(self) -> str:
        """Retrieves and returns the current input value via the 'value' attribute.

        Returns
        -------
        str
        """
        logging.info(
            "Retrieving the value of Input element with locator: %s", self.locator
        )
        return self.get_attribute_value(attribute_name="value")
