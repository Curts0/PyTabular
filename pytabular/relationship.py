"""`relationship.py` houses the main `PyRelationship` and `PyRelationships` class.

Once connected to your model, interacting with relationship(s)
will be done through these classes.
"""
import logging
from object import PyObject, PyObjects
from table import PyTable, PyTables

from Microsoft.AnalysisServices.Tabular import (
    CrossFilteringBehavior,
    SecurityFilteringBehavior,
)

from typing import Union

logger = logging.getLogger("PyTabular")


class PyRelationship(PyObject):
    """The main class for interacting with relationships in your model."""

    def __init__(self, object, model) -> None:
        """Init extends to `PyObject`.

        It also extends a few unique rows to `rich` table.
        A few easy access attributes have been added.
        For example, see `self.From_Table` or `self.To_Column`

        Args:
            object (_type_): _description_
            model (_type_): _description_
        """
        super().__init__(object)
        self.Model = model
        self.CrossFilteringBehavior = CrossFilteringBehavior(
            self.CrossFilteringBehavior.value__
        ).ToString()
        self.SecurityFilteringBehavior = SecurityFilteringBehavior(
            self.SecurityFilteringBehavior.value__
        ).ToString()
        self.To_Table = self.Model.Tables[self.ToTable.Name]
        self.To_Column = self.To_Table.Columns[self.ToColumn.Name]
        self.From_Table = self.Model.Tables[self.FromTable.Name]
        self.From_Column = self.From_Table.Columns[self.FromColumn.Name]
        self._display.add_row("Is Active", str(self.IsActive))
        self._display.add_row("Cross Filtering Behavior", self.CrossFilteringBehavior)
        self._display.add_row(
            "Security Filtering Behavior", self.SecurityFilteringBehavior
        )
        self._display.add_row(
            "From", f"'{self.From_Table.Name}'[{self.From_Column.Name}]"
        )
        self._display.add_row("To", f"'{self.To_Table.Name}'[{self.To_Column.Name}]")


class PyRelationships(PyObjects):
    """Groups together multiple relationships.

    See `PyObjects` class for what more it can do.
    You can interact with `PyRelationships` straight from model.
    For ex: `model.Relationships`.
    """

    def __init__(self, objects) -> None:
        """Init just extends from PyObjects."""
        super().__init__(objects)

    def related(self, object: Union[PyTable, str]) -> PyTables:
        """Finds related tables of a given table.

        Args:
            object (Union[PyTable, str]): `PyTable` or str of table name to find related tables for.

        Returns:
            PyTables: Returns `PyTables` class of the tables in question.
        """
        table_to_find = object if isinstance(object, str) else object.Name
        to_tables = [
            rel.To_Table
            for rel in self._objects
            if rel.From_Table.Name == table_to_find
        ]
        from_tables = [
            rel.From_Table
            for rel in self._objects
            if rel.To_Table.Name == table_to_find
        ]
        to_tables += from_tables
        return PyTables(to_tables)
