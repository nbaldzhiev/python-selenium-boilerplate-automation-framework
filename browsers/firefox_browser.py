"""This module contains an implementation of a Firefox browser."""
from selenium import webdriver

from browsers import BaseBrowser


class FirefoxBrowser(BaseBrowser):
    """This class implements a Firefox browser."""

    def __init__(self):
        super().__init__(driver=webdriver.Firefox())
