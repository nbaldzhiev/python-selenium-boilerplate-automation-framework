""""""
from selenium import webdriver

from browsers import BaseBrowser


class EdgeBrowser(BaseBrowser):
    """"""

    def __init__(self):
        super().__init__(driver=webdriver.Edge())
