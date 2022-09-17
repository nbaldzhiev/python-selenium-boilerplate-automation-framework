"""This module contains an implementation of a Chrome browser."""
from enum import Enum
from typing import List, Tuple, Optional, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from browsers import BaseBrowser, BrowserTypes


class ChromeOptionArguments(Enum):
    """"""
    WINDOW_SIZE = 'window-size'
    DISABLE_INFO_BARS = 'disable-infobars'
    IGNORE_CERT_ERRORS = 'ignore-certificate-errors'


class ChromeBrowser(BaseBrowser):
    """This class implements a Chrome browser."""

    def __init__(
        self, options_args: Optional[List[Tuple[ChromeOptionArguments, Optional[Any]]]] = None
    ):
        options = Options()
        for arg in options_args:
            arg_ = f'--{arg[0]}' if len(arg) == 1 else f'--{arg[0].value}={arg[1]}'
            options.add_argument(argument=arg_)
        super().__init__(browser_type=BrowserTypes.CHROME, options=options)
