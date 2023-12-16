"""`measure.py` houses the main `PyMeasure` and `PyMeasures` class.

Once connected to your model, interacting with measure(s)
will be done through these classes.
"""
import logging
import pandas as pd
from pytabular.object import PyObject, PyObjects
from Microsoft.AnalysisServices.Tabular import Measure, Table


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
            object (object.PyObject): The .Net measure object.
            table (table.PyTable): The parent `PyTable`.
        """
        super().__init__(object)
        self.Table = table
        self._display.add_row("Expression", self._object.Expression, end_section=True)
        self._display.add_row("DisplayFolder", self._object.DisplayFolder)
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("FormatString", self._object.FormatString)

    def get_dependencies(self) -> pd.DataFrame:
        """Get the dependant objects of a measure.

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

    def __init__(self, objects, parent=None) -> None:
        """Extends init from `PyObjects`."""
        super().__init__(objects, parent)

    def __call__(self, *args, **kwargs):
        """Made `PyMeasures` just sends args through to `add_measure`."""
        return self.add_measure(*args, **kwargs)

    def add_measure(
        self, name: str, expression: str, auto_save: bool = True, **kwargs
    ) -> PyMeasure:
        """Add or replace measures from `PyMeasures` class.

        Required is just `name` and `expression`.
        But you can pass through any properties you wish to update as a kwarg.
        This method is also used when calling the class,
        so you can create a new measure that way.
        kwargs will be set via the `settr` built in function.
        Anything in the .Net Measures properties should be viable.
        [Measure Class](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.measure?#properties) # noqa: E501

        Example:
            ```
            expr = "SUM('Orders'[Amount])"
            model.Measures.add_measure("Orders Total", expr)
            ```

            ```
            expr = "SUM('Orders'[Amount])"
            model.Measures.add_measure("Orders Total", expr, Folder = 'Measures')
            ```

            ```
            expr = "SUM('Orders'[Amount])"
            model.Tables['Sales'].Measures('Total Sales', expr, Folder = 'Measures')
            ```

        Args:
            name (str): Name of the measure. Brackets ARE NOT required.
            expression (str): DAX expression for the measure.
            auto_save (bool, optional): Automatically save changes after measure creations.
                Defaults to `True`
        """
        if isinstance(self.parent._object, Table):
            table = self.parent
            model = self.parent.Model
        else:
            table = self.parent.Tables._first_visible_object()
            model = self.parent

        logger.debug(f"Creating measure in {table.Name}")

        new = True

        try:
            logger.debug(f"Measure {name} exists... Overwriting...")
            new_measure = self.parent.Measures[name]._object
            new = False
        except IndexError:
            logger.debug(f"Creating new measure {name}")
            new_measure = Measure()

        new_measure.set_Name(name)
        new_measure.set_Expression(expression)

        for key, value in kwargs.items():
            logger.debug(f"Setting '{key}'='{value}' for {new_measure.Name}")
            setattr(new_measure, key, value)

        if new:
            measures = table.get_Measures()
            measures.Add(new_measure)
        if auto_save:
            model.save_changes()
            return model.Measures[new_measure.Name]
        else:
            return True
