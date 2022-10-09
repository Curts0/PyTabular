import logging

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


class PyMeasures(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
