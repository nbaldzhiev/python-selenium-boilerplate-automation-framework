"""This module contains a base class implementation for a browser."""
from typing import Union
from enum import Enum
import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, Firefox, Edge
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

logging.basicConfig(level=logging.DEBUG)


DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720


class BrowserTypes(Enum):
    """"""
    CHROME = Chrome
    FIREFOX = Firefox
    EDGE = Edge


class BaseBrowser:
    """This class implements a base browser class to be inherited by specific browsers, such as
    Chrome, Firefox, Edge."""

    def __init__(
        self, browser_type: BrowserTypes, options: Union[ChromeOptions, FirefoxOptions, EdgeOptions]
    ):
        self.driver = browser_type.value(options=options)

    def open_url(self, url: str):
        """Opens a url specified by url: str."""
        self.driver.get(url=url)
        logging.info('Opened URL: {}.', url)

    def quit(self):
        """Quits the driver (closes the WebDriver session) and closes all associated windows."""
        self.driver.quit()
        logging.info('Quit the driver and closed all associated windows.')
