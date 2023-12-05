"""`column.py` houses the main `PyColumn` and `PyColumns` class.

Once connected to your model, interacting with column(s) will be done through these classes.
"""
import logging
import pandas as pd
from pytabular.object import PyObject, PyObjects
from Microsoft.AnalysisServices.Tabular import ColumnType

logger = logging.getLogger("PyTabular")


class PyColumn(PyObject):
    """The main class to work with your columns.

    Notice the `PyObject` magic method `__getattr__()` will search in `self._object`
    if it is unable to find it in the default attributes.
    This let's you also easily check the default .Net properties.
    See methods for extra functionality.
    """

    def __init__(self, object, table) -> None:
        """Init that connects your column to parent table.

        It will also build custom rows for your `rich`
        display table.

        Args:
            object (Column): .Net column object.
            table (Table): .Net table object.
        """
        super().__init__(object)
        self.Table = table
        self._display.add_row(
            "Description", str(self._object.Description), end_section=True
        )
        self._display.add_row("DataType", str(self._object.DataType))
        self._display.add_row("EncodingHint", str(self._object.EncodingHint))
        self._display.add_row("IsAvailableInMDX", str(self._object.IsAvailableInMDX))
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("IsKey", str(self._object.IsKey))
        self._display.add_row("IsNullable", str(self._object.IsNullable))
        self._display.add_row("State", str(self._object.State))
        self._display.add_row("DisplayFolder", str(self._object.DisplayFolder))

    def get_dependencies(self) -> pd.DataFrame:
        """Returns the dependant columns of a measure."""
        dmv_query = f"select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY where [OBJECT] = \
            '{self.Name}' and [TABLE] = '{self.Table.Name}'"
        return self.Table.Model.query(dmv_query)

    def get_sample_values(self, top_n: int = 3) -> pd.DataFrame:
        """Get sample values of column."""
        column_to_sample = f"'{self.Table.Name}'[{self.Name}]"
        try:
            # adding temporary try except. TOPNSKIP will not work for directquery mode.
            # Need an efficient way to identify if query is direct query or not.
            dax_query = f"""EVALUATE
                                TOPNSKIP(
                                    {top_n},
                                    0,
                                    FILTER(
                                        VALUES({column_to_sample}),
                                        NOT ISBLANK({column_to_sample})
                                        && LEN({column_to_sample}) > 0
                                    ),
                                    1
                                )
                                ORDER BY {column_to_sample}
                        """
            return self.Table.Model.query(dax_query)
        except Exception:
            # This is really tech debt anyways and should be replaced...
            dax_query = f"""
            EVALUATE
                TOPN(
                    {top_n},
                    FILTER(
                        VALUES({column_to_sample}),
                        NOT ISBLANK({column_to_sample}) && LEN({column_to_sample}) > 0
                    )
                )
            """
            return self.Table.Model.query(dax_query)

    def distinct_count(self, no_blank=False) -> int:
        """Get the `DISTINCTCOUNT` of a column.

        Args:
            no_blank (bool, optional): If `True`, will call `DISTINCTCOUNTNOBLANK`.
                Defaults to `False`.

        Returns:
            int: Number of Distinct Count from column.
                If `no_blank == True` then will return number of distinct count no blanks.
        """
        func = "DISTINCTCOUNT"
        if no_blank:
            func += "NOBLANK"
        return self.Table.Model.Adomd.query(
            f"EVALUATE {{{func}('{self.Table.Name}'[{self.Name}])}}"
        )

    def values(self) -> pd.DataFrame:
        """Get single column DataFrame of values in column.

        Similar to `get_sample_values()` but will return **all**.

        Returns:
            pd.DataFrame: Single column DataFrame of values.
        """
        return self.Table.Model.Adomd.query(
            f"EVALUATE VALUES('{self.Table.Name}'[{self.Name}])"
        )


class PyColumns(PyObjects):
    """Groups together multiple `PyColumn()`.

    See `PyObjects` class for what more it can do.
    You can interact with `PyColumns` straight from model. For ex: `model.Columns`.
    Or through individual tables `model.Tables[TABLE_NAME].Columns`.
    You can even filter down with `.Find()`.
    For example find all columns with `Key` in name.
    `model.Columns.Find('Key')`.
    """

    def __init__(self, objects) -> None:
        """Init extends through to the `PyObjects()` init."""
        super().__init__(objects)

    def query_all(self, query_function: str = "COUNTROWS(VALUES(_))") -> pd.DataFrame:
        """This will dynamically all columns in `PyColumns()` class.

        It will replace the `_` with the column to run
        whatever the given `query_function` value is.

        Args:
                query_function (str, optional): Default is `COUNTROWS(VALUES(_))`.
                        The `_` gets replaced with the column in question.
                        Method will take whatever DAX query is given.

        Returns:
                pd.DataFrame: Returns dataframe with results.
        """
        logger.info("Beginning execution of querying every column...")
        logger.debug(f"Function to be run: {query_function}")
        logger.debug("Dynamically creating DAX query...")
        query_str = "EVALUATE UNION(\n"
        columns = [column for column in self]
        for column in columns:
            if column.Type != ColumnType.RowNumber:
                table_name = column.Table.get_Name()
                column_name = column.get_Name()
                dax_identifier = f"'{table_name}'[{column_name}]"
                query_str += f"ROW(\"Table\",\"{table_name}\",\
                    \"Column\",\"{column_name}\",\"{query_function}\",\
                    {query_function.replace('_',dax_identifier)}), \n"
        query_str = f"{query_str[:-2]})"
        return self[0].Table.Model.query(query_str)
