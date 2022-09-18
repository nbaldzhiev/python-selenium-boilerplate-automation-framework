"""This module contains an implementation of a Chrome browser."""
import logging
from enum import Enum
from typing import Any, List, Optional, Tuple

from selenium.webdriver import Chrome, ChromeOptions

from browsers.base_browser import (
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    BaseBrowser,
)

logging.basicConfig(level=logging.DEBUG)


class ChromeOptionArguments(Enum):
    """Contains constants for option arguments available for Chrome."""

    WINDOW_SIZE = "window-size"
    HEADLESS = "headless"


class ChromeBrowser(BaseBrowser):
    """This class implements a Chrome browser."""

    def __init__(
        self,
        options_args: Optional[
            List[Tuple[ChromeOptionArguments, Optional[Any]]]
        ] = None,
    ):
        options = ChromeOptions()
        if options_args:
            # pylint: disable=duplicate-code
            for arg in options_args:
                arg_ = (
                    f"--{arg[0].value}"
                    if len(arg) == 1
                    else f"--{arg[0].value}={arg[1]}"
                )
                options.add_argument(argument=arg_)
        else:
            # By default, only a resolution is set. Can be updated in case other options are needed
            # to be available by default
            options.add_argument(
                f"--{ChromeOptionArguments.WINDOW_SIZE.value}"
                f"={DEFAULT_WINDOW_WIDTH},{DEFAULT_WINDOW_HEIGHT}"
            )

        super().__init__(driver=Chrome(options=options))
        logging.info(
            "Started a Chrome browser with the following options: %s.",
            options._arguments,
        )
