"""
`measure.py` houses the main `PyMeasure` and `PyMeasures` class.
Once connected to your model, interacting with measure(s) will be done through these classes.
"""
import logging
import pandas as pd
from object import PyObject, PyObjects

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
        self._display.add_row("Expression", self._object.Expression, end_section=True)
        self._display.add_row("DisplayFolder", self._object.DisplayFolder)
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("FormatString", self._object.FormatString)

    def get_dependencies(self) -> pd.DataFrame:
        """Returns the dependant columns of a measure"""
        dmv_query = f"select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY where [OBJECT] = '{self.Name}' and [TABLE] = '{self.Table.Name}'"
        return self.Table.Model.Query(dmv_query)


class PyMeasures(PyObjects):
    """
    Groups together multiple measures. See `PyObjects` class for what more it can do.
    You can interact with `PyMeasures` straight from model. For ex: `model.Measures`.
    Or through individual tables `model.Tables[TABLE_NAME].Measures`.
    You can even filter down with `.Find()`. For example find all measures with `ratio` in name.
    `model.Measures.Find('ratio')`.
    """

    def __init__(self, objects) -> None:
        super().__init__(objects)
