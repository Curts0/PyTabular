import logging

from object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd
from typing import List
logger = logging.getLogger("PyTabular")

class PyPartition(PyObject):
    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table
    def Last_Refresh(self):
        return ticks_to_datetime(self.RefreshedTime.Ticks)
    def Refresh(self, *args, **kwargs) -> pd.DataFrame:
        '''Same method from Model Refresh, you can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Partitions[0].Refresh(Tracing = True)`
        Returns: 
            pd.DataFrame: Returns pandas dataframe with some refresh details
        '''        
        return self.Table.Model.Refresh(self._object, *args, **kwargs)

class PyPartitions(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)