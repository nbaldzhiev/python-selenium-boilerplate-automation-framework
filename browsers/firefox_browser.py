"""This module contains an implementation of a Firefox browser."""
import logging
from enum import Enum
from typing import Any, List, Optional, Tuple

from selenium.webdriver import Firefox, FirefoxOptions

from browsers.base_browser import (
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    BaseBrowser,
)

logging.basicConfig(level=logging.DEBUG)


class FirefoxOptionArguments(Enum):
    """Contains constants for option arguments available for Firefox.

    Examples
    --------
        browser = FirefoxBrowser()
        browser = FirefoxBrowser(
            option_args=[
                (FirefoxOptionArguments.WIDTH, '640'),
                (FirefoxOptionArguments.HEIGHT, '480'),
                (FirefoxOptionArguments.HEADLESS, ),
            ]
        )
    """

    WIDTH = "width"
    HEIGHT = "height"
    HEADLESS = "headless"


class FirefoxBrowser(BaseBrowser):
    """This class implements a Firefox browser."""

    def __init__(
        self,
        options_args: Optional[
            List[Tuple[FirefoxOptionArguments, Optional[Any]]]
        ] = None,
    ):
        options = FirefoxOptions()
        if options_args:
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
            options._arguments.extend(
                [
                    f"--{FirefoxOptionArguments.WIDTH.value}={DEFAULT_WINDOW_WIDTH}",
                    f"--{FirefoxOptionArguments.HEIGHT.value}={DEFAULT_WINDOW_HEIGHT}",
                ]
            )

        super().__init__(driver=Firefox(options=options))
        logging.info(
            "Started a Firefox browser with the following options: %s.",
            options._arguments,
        )
