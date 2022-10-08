import logging

from object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd

logger = logging.getLogger("PyTabular")


class PyPartition(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Partition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition?view=analysisservices-dotnet).
    With a few other bells and whistles added to it. WIP

    Args:
        Table: Parent Table to the Column
    """

    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table

    def Last_Refresh(self):
        """Queries `RefreshedTime` attribute in the partition and converts from C# Ticks to Python datetime

        Returns:
            datetime.datetime: Last Refreshed time of Partition in datetime format
        """
        return ticks_to_datetime(self.RefreshedTime.Ticks)

    def Refresh(self, *args, **kwargs) -> pd.DataFrame:
        """Same method from Model Refresh, you can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Partitions[0].Refresh(Tracing = True)`
        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details
        """
        return self.Table.Model.Refresh(self._object, *args, **kwargs)


class PyPartitions(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
