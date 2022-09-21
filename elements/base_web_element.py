"""This module contains an implementation of a base web element class."""
from __future__ import annotations

import logging
from typing import Optional, Tuple, Union

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)
DEFAULT_DISPLAYED_WAIT = 60  # seconds


class BaseWebElement:
    """This class implements a base web element class to be inherited by specific web elements,
    such as buttons, dropdowns, tables, etc."""

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Optional[Tuple[By, str]] = None,
        web_element: Optional[WebElement] = None,
    ):
        self._parent = parent
        self.locator = locator
        self.web_element = web_element

    @property
    def parent(self) -> Union[WebDriver, WebElement]:
        """Returns the parent as either a WebDriver or WebElement object.

        Returns
        -------
        Union[WebDriver, WebElement]
        """
        if isinstance(self._parent, BaseWebElement):
            return self._parent.find_element()
        return self._parent

    def find_element(self, wait_until_is_present: bool = True) -> WebElement:
        """Finds an element and returns it as a WebElement object.

        Parameters
        ----------
        wait_until_is_present : bool
            Controls whether the method first waits for the web element to be present.
            Defaults to True.

        Returns
        -------
        WebElement
        """
        if self.web_element:
            # Check if the element is stale first before returning it
            try:
                _ = self.web_element.location
            except StaleElementReferenceException as exc:
                if not self.locator:
                    raise UserWarning(
                        "The web element is stale and a locator was not provided, "
                        "hence it is not possible to find it!"
                    ) from exc
            else:
                return self.web_element

        if wait_until_is_present:
            logging.info(
                "Starting to wait for element with locator %s to be present",
                self.locator,
            )
            WebDriverWait(self.parent, DEFAULT_DISPLAYED_WAIT).until(
                method=lambda parent: parent.find_element(*self.locator),
                message=f"Could not wait for the element with locator {self.locator} to be "
                f"present! Tried for {DEFAULT_DISPLAYED_WAIT} seconds",
            )

        logging.info("Got element with locator: %s.", self.locator)
        self.web_element = self.parent.find_element(*self.locator)
        return self.web_element

    def get_attribute_value(self, attribute_name: str):
        """Returns the value of the tag's attribute specified by attribute_name: str."""
        return self.find_element().get_attribute(name=attribute_name)

    def click(self):
        """Clicks on the WebElement."""
        self.find_element().click()
        logging.info("Clicked on element with locator: %s.", self.locator)

    def is_enabled(self) -> bool:
        """Determines whether the web element is enabled or not.

        Returns
        -------
        bool
        """
        return self.find_element().is_enabled()

    @property
    def element_screenshot_as_base64(self) -> str:
        """Returns a screenshot of the web element as a base64 encoded string.

        Returns
        -------
        str
        """
        logging.info("Taking a screenshot of element with locator: %s.", self.locator)
        return self.find_element().screenshot_as_base64

    @property
    def text(self) -> str:
        """The text of the web element.

        Returns
        -------
        str
        """
        return self.find_element().text
