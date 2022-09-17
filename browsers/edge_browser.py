"""This module contains an implementation of a Microsoft Edge browser."""
from selenium import webdriver

from browsers import BaseBrowser


class EdgeBrowser(BaseBrowser):
    """This class implements a Microsoft Edge browser."""

    def __init__(self):
        super().__init__(driver=webdriver.Edge())
