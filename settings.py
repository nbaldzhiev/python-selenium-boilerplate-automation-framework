"""Contains common settings across the project."""
from logging import INFO

from selenium.webdriver.remote.webdriver import WebDriver

LOGGING_LEVEL = INFO
GLOBAL_DRIVER: WebDriver


def set_global_driver(driver: WebDriver):
    """Sets the GLOBAL_DRIVER so it can be used cross-module.

    Parameters
    ----------
    driver : WebDriver
        The WebDriver whose value is to be saved to GLOBAL_DRIVER. This is currently only done
        from the constructor of the BaseBrowser class.
    """
    # pylint: disable=global-statement
    global GLOBAL_DRIVER
    GLOBAL_DRIVER = driver
