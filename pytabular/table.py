import logging
from object import PyObject
import pandas as pd
from partition import PyPartition, PyPartitions
from column import PyColumn, PyColumns
from measure import PyMeasure, PyMeasures
from pytabular.object import PyObjects
from logic_utils import ticks_to_datetime

logger = logging.getLogger("PyTabular")


class PyTable(PyObject):
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
        self.Partitions = PyPartitions(
            [
                PyPartition(partition, self)
                for partition in self._object.Partitions.GetEnumerator()
            ]
        )
        self.Columns = PyColumns(
            [PyColumn(column, self) for column in self._object.Columns.GetEnumerator()]
        )
        self.Measures = PyMeasures(
            [
                PyMeasure(measure, self)
                for measure in self._object.Measures.GetEnumerator()
            ]
        )
        self._display.add_row("# of Partitions", str(len(self.Partitions)))
        self._display.add_row("# of Columns", str(len(self.Columns)))
        self._display.add_row(
            "# of Measures", str(len(self.Measures)), end_section=True
        )
        self._display.add_row("Description", self._object.Description, end_section=True)
        self._display.add_row("DataCategory", str(self._object.DataCategory))
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("IsPrivate", str(self._object.IsPrivate))
        self._display.add_row(
            "ModifiedTime",
            ticks_to_datetime(self._object.ModifiedTime.Ticks).strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
        )

    def Row_Count(self) -> int:
        """Method to return count of rows. Simple Dax Query:
        `EVALUATE {COUNTROWS('Table Name')}`

        Returns:
            int: Number of rows using [COUNTROWS](https://learn.microsoft.com/en-us/dax/countrows-function-dax).
        """
        return self.Model.Adomd.Query(f"EVALUATE {{COUNTROWS('{self.Name}')}}")

    def Refresh(self, *args, **kwargs) -> pd.DataFrame:
        """Same method from Model Refresh, you can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Refresh(Tracing = True)`
        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details
        """
        return self.Model.Refresh(self.Name, *args, **kwargs)


class PyTables(PyObjects):
    """Iterator to handle tables. Accessible via `Tables` attribute in Tabular class.

    Args:
        PyTable: PyTable class
    """

    def __init__(self, objects) -> None:
        super().__init__(objects)
