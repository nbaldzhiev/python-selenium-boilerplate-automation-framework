""""""
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions

from browsers import BaseBrowser


class ChromeBrowser(BaseBrowser):
    """"""

    def __init__(self):
        super().__init__(driver=webdriver.Chrome())
