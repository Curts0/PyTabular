import logging
from object import PyObject
from pytabular.object import PyObjects
from pytabular.table import PyTable, PyTables
from pytabular.column import PyColumn, PyColumns
from Microsoft.AnalysisServices.Tabular import (
    CrossFilteringBehavior,
    SecurityFilteringBehavior
)

from typing import Union

logger = logging.getLogger("PyTabular")


class PyRelationship(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Tabular.Table](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.table?view=analysisservices-dotnet).
    With a few other bells and whistles added to it. You can use the table to access the nested Columns and Partitions. WIP

    Attributes:
        Model: Reference to Tabular class
        Partitions: Reference to Table Partitions
        Columns: Reference to Table Columns
    """

    def __init__(self, object, model) -> None:
        super().__init__(object)
        self.Model = model
        self.CrossFilteringBehavior = CrossFilteringBehavior(self.CrossFilteringBehavior.value__).ToString()
        self.SecurityFilteringBehavior = SecurityFilteringBehavior(self.SecurityFilteringBehavior.value__).ToString()
        self.To_Table = self.Model.Tables[self.ToTable.Name]
        self.To_Column = self.To_Table.Columns[self.ToColumn.Name]
        self.From_Table = self.Model.Tables[self.FromTable.Name]
        self.From_Column = self.From_Table.Columns[self.FromColumn.Name]
        self._display.add_row("Is Active", str(self.IsActive))
        self._display.add_row("Cross Filtering Behavior", self.CrossFilteringBehavior)
        self._display.add_row("Security Filtering Behavior", self.SecurityFilteringBehavior)
        self._display.add_row("From", f"'{self.From_Table.Name}'[{self.From_Column.Name}]")
        self._display.add_row("To", f"'{self.To_Table.Name}'[{self.To_Column.Name}]")


class PyRelationships(PyObjects):
    """Iterator to handle tables. Accessible via `Tables` attribute in Tabular class.

    Args:
        PyTable: PyTable class
    """

    def __init__(self, objects) -> None:
        super().__init__(objects)
    def Related(self, object: Union[PyTable, str]):
        table_to_find = object if isinstance(object, str) else object.Name
        to_tables = [rel.To_Table for rel in self._objects if rel.From_Table.Name == table_to_find]
        from_tables = [rel.From_Table for rel in self._objects if rel.To_Table.Name == table_to_find]
        to_tables += from_tables
        return  PyTables(to_tables)
