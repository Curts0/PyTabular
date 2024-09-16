"""`partition.py` houses the main `PyPartition` and `PyPartitions` class.

Once connected to your model, interacting with partition(s) will be done through these classes.
"""

import logging

from pytabular.object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd
from datetime import datetime

logger = logging.getLogger("PyTabular")


class PyPartition(PyObject):
    """Main class for interacting with partitions.

    See methods for available uses.
    """

    def __init__(self, object, table) -> None:
        """Extends from `PyObject` class.

        Adds a few custom rows to `rich` table for the partition.

        Args:
            object (Partition): .Net Partition object.
            table (PyTable): Parent table of the partition in question.
        """
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
        """Queries `RefreshedTime` attribute in the partition.

        Converts from C# Ticks to Python datetime.

        Returns:
            datetime.datetime: Last Refreshed time of Partition in datetime format
        """
        return ticks_to_datetime(self.RefreshedTime.Ticks)

    def refresh(self, *args, **kwargs) -> pd.DataFrame:
        """Same method from Model Refresh.

        You can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Partitions[0].refresh()`

        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details
        """
        return self.Table.Model.refresh(self, *args, **kwargs)


class PyPartitions(PyObjects):
    """Groups together multiple partitions.

    See `PyObjects` class for what more it can do.
    You can interact with `PyPartitions` straight from model.
    For ex: `model.Partitions`.
    Or through individual tables `model.Tables[TABLE_NAME].Partitions`.
    You can even filter down with `.find()`. For example find partitions with `prev-year` in name.
    `model.Partitions.find('prev-year')`.
    """

    def __init__(self, objects) -> None:
        """Extends through to `PyObjects`."""
        super().__init__(objects)

    def refresh(self, *args, **kwargs):
        """Refreshes all `PyPartition`(s) in class."""
        model = self[0].Table.Model
        return model.refresh(self, *args, **kwargs)
