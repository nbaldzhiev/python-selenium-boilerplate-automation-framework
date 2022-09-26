"""This module contains an implementation of a collection of web elements, i.e. multiple elements
with a common locator under a given parent"""
import logging
from typing import List, Tuple, Type, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class Collection:
    """This class implements a Collection, which represents multiple elements with a common
    locator situated under a given parent.

    Examples
    --------
        row_data_cells = Collection(
            parent=row, children_locator=(By.CSS_SELECTOR, "td")
        )
        checkboxes = Collection(
            parent=browser.driver,
            children_locator=(By.CSS_SELECTOR, 'input[type="checkbox"]',
            children_cls=Input,
        )
    """

    def __init__(
        self,
        parent: Union[BaseWebElement, WebElement, WebDriver],
        children_locator: Tuple[By, str],
        children_cls: Type[BaseWebElement] = BaseWebElement,
    ):
        self._parent = parent
        self.children_locator = children_locator
        self.children_cls = children_cls
        self.web_elements: List = []

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

    def find_elements(self) -> List[BaseWebElement]:
        """Finds all elements with the parent and locator, specified in the constructor, and
        returns them as a list of objects of type children_cls.

        Returns
        -------
        List[BaseWebElement]
        """
        cls_elements = [
            self.children_cls(web_element=elem)
            for elem in self.parent.find_elements(*self.children_locator)
        ]
        logging.info("Got a Collection with the following elements: %s", cls_elements)
        self.web_elements = cls_elements
        return cls_elements
