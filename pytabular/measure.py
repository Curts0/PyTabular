"""`measure.py` houses the main `PyMeasure` and `PyMeasures` class.

Once connected to your model, interacting with measure(s)
will be done through these classes.
"""
import logging
import pandas as pd
from object import PyObject, PyObjects

logger = logging.getLogger("PyTabular")


class PyMeasure(PyObject):
    """Main class for interacting with measures.

    See methods for available functionality.
    """

    def __init__(self, object, table) -> None:
        """Connects measure to parent `PyTable`.

        It will also add some custom rows for the `rich`
        table display.

        Args:
            object: The .Net measure object.
            table (PyTable): The parent `PyTable`.
        """
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
        dmv_query = f"select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY where \
            [OBJECT] = '{self.Name}' and [TABLE] = '{self.Table.Name}'"
        return self.Table.Model.query(dmv_query)


class PyMeasures(PyObjects):
    """Groups together multiple measures.

    See `PyObjects` class for what more it can do.
    You can interact with `PyMeasures` straight from model. For ex: `model.Measures`.
    Or through individual tables `model.Tables[TABLE_NAME].Measures`.
    You can even filter down with `.find()`.
    For example find all measures with `ratio` in name.
    `model.Measures.find('ratio')`.
    """

    def __init__(self, objects) -> None:
        """Extends init from `PyObjects`."""
        super().__init__(objects)
