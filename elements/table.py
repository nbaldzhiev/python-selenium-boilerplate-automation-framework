"""This module contains an implementation of a table type of element in a given UI."""
from __future__ import annotations

import logging
from typing import List, Optional, Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from elements.base_web_element import BaseWebElement
from elements.collection import Collection
from settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)


class TableColumn(BaseWebElement):
    """This class implements an abstraction of a table column type of element in a UI."""

    def __init__(
        self,
        header_cell: Union[BaseWebElement, WebElement],
        body_cells: List[Union[BaseWebElement, WebElement]],
        parent: Optional[Union[BaseWebElement, WebElement]] = None,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, web_element=web_element)
        self.header_cell = header_cell
        self.body_cells = body_cells

    @property
    def column_title(self) -> str:
        """Returns the title of the column, which is the text contained in the header cell of the
        column.

        Returns
        -------
        str
        """
        return self.header_cell.text

    def get_cell_by_row_index(self, row_index: int) -> BaseWebElement:
        """Gets and returns the cell at row identified by row_index.

        Parameters
        ----------
        row_index : int
            A 1-based index identifying whose row's data cell to return. For example, row_index=3
            would return the 3rd row's cell.

        Returns
        -------
        BaseWebElement
            The data cell as a BaseWebElement object or another object, which is an instance of
            BaseWebElement.
        """
        return self.body_cells[row_index - 1]

    def get_cell_text_by_row_index(self, row_index: int) -> str:
        """Gets and returns the text of the cell located at the row identified by row_index.

        Parameters
        ----------
        row_index : int
            A 1-based index identifying whose row's data cell to return. For example, row_index=3
            would return the 3rd row's cell.

        Returns
        -------
        str
        """
        return self.get_cell_by_row_index(row_index=row_index).text


class Table(BaseWebElement):
    """This class implements an abstraction of a table type of element in a UI.

    Examples
    --------
        table = Table(parent=some_browser.driver)
        table = Table(parent=some_element)
    """

    # A default locator to allow for a simpler interface where the user only passes the
    # parent element. Set the value to a common selector for table elements in your project
    DEFAULT_LOCATOR = (By.CSS_SELECTOR, "table")

    def __init__(
        self,
        parent: Optional[Union[BaseWebElement, WebElement, WebDriver]] = None,
        locator: Tuple[By, str] = DEFAULT_LOCATOR,
        web_element: Optional[WebElement] = None,
    ):
        super().__init__(parent=parent, locator=locator, web_element=web_element)

    @property
    def columns(self):
        """Returns the columns of the table.

        Returns
        -------
        List[TableColumn]
            The table's columns as a list of TableColumn objects.
        """
        columns: List = []

        header_cells = Collection(
            parent=self, children_locator=(By.CSS_SELECTOR, "thead > tr > th")
        ).find_elements()
        body_rows = Collection(
            parent=self, children_locator=(By.CSS_SELECTOR, "tbody > tr")
        ).find_elements()
        for h_cell in header_cells:
            kwargs = {"header_cell": h_cell}
            body_cells = []
            for row in body_rows:
                row_data_cells = Collection(
                    parent=row, children_locator=(By.CSS_SELECTOR, "td")
                ).find_elements()
                body_cells.append(row_data_cells[header_cells.index(h_cell)])
            kwargs["body_cells"] = body_cells
            columns.append(TableColumn(**kwargs))

        return columns

    def get_column_by_column_title(self, column_title: str) -> TableColumn:
        """Gets and returns the column with a header title specified by column_title.

        Parameters
        ----------
        column_title : str
            The header title of the column.

        Returns
        -------
        TableColumn
            The column as TableColumn object.
        """
        try:
            col = list(
                filter(
                    lambda col: col.column_title.lower() == column_title.lower(),
                    self.columns,
                )
            )[0]
            logging.info("Got table column with title: %s.", column_title)
        except IndexError as exc:
            raise IndexError(
                f"A column with title {column_title} was not found!"
            ) from exc
        else:
            return col
