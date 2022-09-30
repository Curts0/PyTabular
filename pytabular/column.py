import logging

from object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd
from typing import List
logger = logging.getLogger("PyTabular")

class PyColumn(PyObject):
    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table
    def Distinct_Count(self, No_Blank = False):
        func = 'DISTINCTCOUNT'
        if No_Blank:
            func += 'NOBLANK'
        return self.Table.Model.Adomd.Query(f"EVALUATE {{{func}('{self.Table.Name}'[{self.Name}])}}")

class PyColumns(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)