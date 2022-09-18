"""This module contains a base class implementation for a browser."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720


class BaseBrowser:
    """This class implements a base browser class to be inherited by specific browsers, such as
    Chrome, Firefox, Edge."""

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

    def open_url(self, url: str):
        """Opens a url specified by url: str."""
        self.driver.get(url=url)
        logging.info("Opened URL: %s.", url)

    def quit(self):
        """Quits the driver (closes the WebDriver session) and closes all associated windows."""
        self.driver.quit()
        logging.info("Quit the driver and closed all associated windows.")
