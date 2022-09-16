""""""
from selenium import webdriver

from browsers import BaseBrowser


class FirefoxBrowser(BaseBrowser):
    """"""

    def __init__(self):
        super().__init__(driver=webdriver.Firefox())
