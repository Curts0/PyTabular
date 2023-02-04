"""
`partition.py` houses the main `PyPartition` and `PyPartitions` class.
Once connected to your model, interacting with partition(s) will be done through these classes.
"""
import logging

from object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd
from datetime import datetime

logger = logging.getLogger("PyTabular")


class PyPartition(PyObject):
    """Wrapper for [Partition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition?view=analysisservices-dotnet).
    With a few other bells and whistles added to it.

    Args:
        Table: Parent Table to the Column
    """

    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table
        self._display.add_row("Mode", str(self._object.Mode))
        self._display.add_row("State", str(self._object.State))
        self._display.add_row(
            "SourceType", str(self._object.SourceType), end_section=True
        )
        self._display.add_row(
            "RefreshedTime", self.last_refresh().strftime("%m/%d/%Y, %H:%M:%S")
        )

    def last_refresh(self) -> datetime:
        """Queries `RefreshedTime` attribute in the partition and converts from C# Ticks to Python datetime

        Returns:
            datetime.datetime: Last Refreshed time of Partition in datetime format
        """
        return ticks_to_datetime(self.RefreshedTime.Ticks)

    def refresh(self, *args, **kwargs) -> pd.DataFrame:
        """Same method from Model Refresh, you can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Partitions[0].refresh(Tracing = True)`
        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details
        """
        return self.Table.Model.refresh(self, *args, **kwargs)


class PyPartitions(PyObjects):
    """
    Groups together multiple partitions. See `PyObjects` class for what more it can do.
    You can interact with `PyPartitions` straight from model. For ex: `model.Partitions`.
    Or through individual tables `model.Tables[TABLE_NAME].Partitions`.
    You can even filter down with `.Find()`. For example find all partition with `prev-year` in name.
    `model.Partitions.Find('prev-year')`.
    """

    def __init__(self, objects) -> None:
        super().__init__(objects)
