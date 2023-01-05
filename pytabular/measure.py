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
        """Returns the dependant objects of a measure.
        Args:
            self: The Measure Object

        Returns:
            pd.DataFrame: The Return Value is a Pandas dataframe
                            which displays all the dependancies 
                            of the object.             

        """
        dmv_query = f"select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY where [OBJECT] = '{self.Name}' and [TABLE] = '{self.Table.Name}'"
        return self.Table.Model.Query(dmv_query)


class PyMeasures(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
