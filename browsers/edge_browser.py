"""This module contains an implementation of an Edge browser."""
import logging
from enum import Enum
from typing import Any, List, Optional, Tuple

from selenium.webdriver import Edge, EdgeOptions

from browsers.base_browser import BaseBrowser

logging.basicConfig(level=logging.DEBUG)


class EdgeOptionArguments(Enum):
    """Contains constants for option arguments available for Edge."""

    # TODO: Find out and add the window size argument values
    HEADLESS = "headless"


class EdgeBrowser(BaseBrowser):
    """This class implements a Microsoft Edge browser."""

    def __init__(
        self,
        options_args: Optional[List[Tuple[EdgeOptionArguments, Optional[Any]]]] = None,
    ):
        options = EdgeOptions()
        if options_args:
            for arg in options_args:
                # TODO: add proper formatting of options with values as currently I can't find an
                #  example of an option argument with value, i.e. window size, for Edge
                options.add_argument(argument=arg[0].value)
        else:
            # TODO: add default resolution arguments
            pass

        super().__init__(driver=Edge(options=options))
        logging.info(
            "Started an Edge browser with the following options: %s.",
            options._arguments,
        )
