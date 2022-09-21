"""This module contains an abstraction of base dropdown."""
from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple, Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from elements.collection import Collection
from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class BaseDropdown(BaseWebElement, metaclass=ABCMeta):
    """This class implements an abstraction of a dropdown type of element."""

    def __init__(
        self,
        locator: Tuple[By, str],
        expanded_locator: Tuple[By, str],
        expanded_options_loc: Tuple[By, str],
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, locator=locator, web_element=web_element)
        self._expanded_locator = expanded_locator
        self._expanded_options_locator = expanded_options_loc

    @property
    @abstractmethod
    def expanded(self):
        """An abstract method which needs to be implemented by each type of dropdown - single
        select, multi select, etc."""

    def is_expanded(self) -> bool:
        """Determines whether the dropdown is currently expanded or not.

        Returns
        -------
        bool
        """
        return (
            "true" in self.get_attribute_value(attribute_name="aria-expanded").lower()
        )

    def expand_dropdown(self, on_hover: bool = False):
        """Expands the dropdown and returns its expanded container.

        Parameters
        ----------
        on_hover : bool
            Controls whether the dropdown is expanded via a hover. If False, then the dropdown
            button is clicked, instead of hovered on. Defaults to False.
        """
        from settings import GLOBAL_DRIVER

        if not self.is_expanded():
            if on_hover:
                ActionChains(GLOBAL_DRIVER).move_to_element(
                    self.find_element()
                ).perform()
            else:
                self.click()
            logging.info("Expanded dropdown with locator: %s.", self.locator)
        return self.expanded


class BaseExpandedDropdown(BaseWebElement):
    """This class contains an abstraction of a base expanded dropdown."""

    # Maximum time to wait for the options to have a value as some sites tend to load slowly
    OPTIONS_VALUES_TIMEOUT = 10  # seconds
    OPTIONS_VALUES_INTERVAL = 1  # seconds

    def __init__(
        self,
        locator: Tuple[By, str],
        options_locator: Tuple[By, str],
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, locator=locator, web_element=web_element)
        self.options_locator = options_locator

    @property
    def options_as_web_elements(self) -> List[BaseWebElement]:
        """

        Returns
        -------
        List[BaseWebElement]
            The options of the dropdown as a list of BaseWebElement[s].
        """
        import time

        self.find_element()

        # The waiting mechanism below is added to support some slow sites which tend to take some
        # time before the list of dropdown options actually loads together with the option values,
        # after expanding the dropdown
        timeout = time.time() + type(self).OPTIONS_VALUES_TIMEOUT
        while time.time() < timeout:
            options = Collection(
                # If the expanded dropdown container element is not a child of the dropdown itself,
                # modify the parent argument to pass the driver instead (import the global one)
                parent=self.find_element(),
                children_locator=self.options_locator,
            ).find_elements()
            filtered = list(filter(lambda opt: not opt.text, options))

            if not options or filtered:
                time.sleep(type(self).OPTIONS_VALUES_INTERVAL)
            else:
                logging.info(
                    "Got the options of expanded dropdown with locator: %s.",
                    self.locator,
                )
                return options

    @property
    def options_as_strings(self) -> List[str]:
        """

        Returns
        -------
        List[str]
            The options of the dropdown as a list of strings.
        """
        return [element.text for element in self.options_as_web_elements]
