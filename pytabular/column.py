"""`column.py` houses the main `PyColumn` and `PyColumns` class.
Once connected to your model, interacting with column(s) will be done through these classes.
"""
import logging
import pandas as pd
from object import PyObject, PyObjects
from Microsoft.AnalysisServices.Tabular import ColumnType

logger = logging.getLogger("PyTabular")


class PyColumn(PyObject):
    """Wrapper for [Column](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column?view=analysisservices-dotnet).
    With a few other bells and whistles added to it.
    Notice the `PyObject` magic method `__getattr__()` will search in `self._object`
    if it is unable to find it in the default attributes.
    This let's you also easily check the default .Net properties.

    Args:
        Table: Parent Table to the Column
    """

    def __init__(self, object, table) -> None:
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
        """Returns the dependant columns of a measure"""
        dmv_query = f"select * from $SYSTEM.DISCOVER_CALC_DEPENDENCY where [OBJECT] = '{self.Name}' and [TABLE] = '{self.Table.Name}'"
        return self.Table.Model.Query(dmv_query)

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
                                        NOT ISBLANK({column_to_sample}) && LEN({column_to_sample}) > 0
                                    ),
                                    1
                                )
                                ORDER BY {column_to_sample}
                        """
            return self.Table.Model.Query(dax_query)
        except Exception:  # pragma: no cover
            # Excluding exception from coverage.py for now...
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
            return self.Table.Model.Query(dax_query)

    def Distinct_Count(self, No_Blank=False) -> int:
        """Get [DISTINCTCOUNT](https://learn.microsoft.com/en-us/dax/distinctcount-function-dax) of Column.

        Args:
            No_Blank (bool, optional): Ability to call [DISTINCTCOUNTNOBLANK](https://learn.microsoft.com/en-us/dax/distinctcountnoblank-function-dax). Defaults to False.

        Returns:
            int: Number of Distinct Count from column. If `No_Blank == True` then will return number of Distinct Count no blanks.
        """
        func = "DISTINCTCOUNT"
        if No_Blank:
            func += "NOBLANK"
        return self.Table.Model.Adomd.Query(
            f"EVALUATE {{{func}('{self.Table.Name}'[{self.Name}])}}"
        )

    def Values(self) -> pd.DataFrame:
        """Get single column DataFrame of [VALUES](https://learn.microsoft.com/en-us/dax/values-function-dax)

        Returns:
            pd.DataFrame: Single Column DataFrame of Values.
        """
        return self.Table.Model.Adomd.Query(
            f"EVALUATE VALUES('{self.Table.Name}'[{self.Name}])"
        )


class PyColumns(PyObjects):
    """Groups together multiple columns. See `PyObjects` class for what more it can do.
    You can interact with `PyColumns` straight from model. For ex: `model.Columns`.
    Or through individual tables `model.Tables[TABLE_NAME].Columns`.
    You can even filter down with `.Find()`. For example find all columns with `Key` in name.
    `model.Columns.Find('Key')`.
    """

    def __init__(self, objects) -> None:
        super().__init__(objects)

    def Query_All(self, query_function: str = "COUNTROWS(VALUES(_))") -> pd.DataFrame:
        """This will dynamically create a query to pull all columns from the model and run the query function.
        It will replace the _ with the column to run.

        Args:
                query_function (str, optional): Dax query is dynamically building a query with the UNION & ROW DAX Functions.

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
                query_str += f"ROW(\"Table\",\"{table_name}\",\"Column\",\"{column_name}\",\"{query_function}\",{query_function.replace('_',dax_identifier)}),\n"
        query_str = f"{query_str[:-2]})"
        return self[0].Table.Model.Query(query_str)
