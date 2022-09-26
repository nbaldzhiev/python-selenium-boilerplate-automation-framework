"""This module contains an implementation of a button type of element in a given UI."""
from typing import Optional, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement


class Button(BaseWebElement):
    """This class implements an abstraction of a button type of element in a UI.

    Examples
    --------
        button = Button(parent=some_browser.driver)
        button = Button(parent=some_element, locator=(By.CSS_LOCATOR, 'button[class$="-submit"]'))
    """

    # A default locator to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for button elements in your project
    DEFAULT_LOCATOR = (By.CSS_SELECTOR, "button")

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Tuple[By, str] = DEFAULT_LOCATOR,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, locator=locator, web_element=web_element)
