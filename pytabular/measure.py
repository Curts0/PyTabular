import logging

from object import PyObject, PyObjects
from logic_utils import ticks_to_datetime
import pandas as pd

logger = logging.getLogger("PyTabular")


class PyMeasure(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Measure](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet).
    With a few other bells and whistles added to it. WIP

    Args:
        Table: Parent Table to the Measure
    """

    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table


class PyMeasures(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
