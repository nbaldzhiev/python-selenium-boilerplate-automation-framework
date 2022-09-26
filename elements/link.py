"""This module contains an implementation of a link type of element in a given UI."""
from typing import Optional, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement


class Link(BaseWebElement):
    """This class implements an abstraction of a link type of element in a UI.

    Examples
    --------
        link = Link(parent=some_browser.driver)
        link = Link(parent=some_element, locator=(By.CSS_LOCATOR, 'a#reset-password'))
    """

    # A default locator to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for link elements in your project
    DEFAULT_LOCATOR = (By.CSS_SELECTOR, "a")

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Tuple[By, str] = DEFAULT_LOCATOR,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, locator=locator, web_element=web_element)

    def is_active(self) -> bool:
        """Determines whether the link is active or not, i.e. is it currently selected or not.

        Returns
        -------
        bool
        """
        return "active" in self.get_attribute_value("class").lower()

    def open_link(self):
        """Opens the link by clicking on the element."""
        if not self.is_active():
            self.click()
