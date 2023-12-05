"""`table.py` houses the main `PyTable` and `PyTables` class.

Once connected to your model, interacting with table(s) will be done through these classes.
"""
import logging
import pandas as pd
from pytabular.partition import PyPartition, PyPartitions
from pytabular.column import PyColumn, PyColumns
from pytabular.measure import PyMeasure, PyMeasures
from pytabular.object import PyObjects, PyObject
from logic_utils import ticks_to_datetime
from datetime import datetime

logger = logging.getLogger("PyTabular")


class PyTable(PyObject):
    """The main PyTable class to interact with the tables in model.

    Attributes:
        Name (str): Name of table.
        IsHidden (bool): Is the table hidden.
        Description (str): The description of the table.
        Model (Tabular): The parent `Tabular()` class.
        Partitions (PyPartitions): The `PyPartitions()` in the table.
        Columns (PyColumns): The `PyColumns()` in the table.
        Measures (PyMeasures): The `PyMeasures()` in the table.

    Example:
        ```python title="Passing through PyTable to PyPartition"

        model.Tables[0].Partitions['Last Year'].refresh() # (1)
        ```

        1. This shows the ability to travel through your model
        to a specific partition and then running a refresh
        for that specific partition.
        `model` -> `PyTables` -> `PyTable` (1st index) -> `PyPartitions`
        -> `PyPartition` (.Name == 'Last Year') -> `.refresh()`
    """

    def __init__(self, object, model) -> None:
        """Init extends from `PyObject` class.

        Also adds a few specific rows to the `rich`
        table.

        Args:
            object (Table): The actual .Net table.
            model (Tabular): The model that the table is in.
        """
        super().__init__(object)
        self.Model = model
        self.Partitions: PyPartitions = PyPartitions(
            [
                PyPartition(partition, self)
                for partition in self._object.Partitions.GetEnumerator()
            ]
        )
        self.Columns: PyColumns = PyColumns(
            [PyColumn(column, self) for column in self._object.Columns.GetEnumerator()]
        )
        self.Measures: PyMeasures = PyMeasures(
            [
                PyMeasure(measure, self)
                for measure in self._object.Measures.GetEnumerator()
            ],
            self,
        )
        self._display.add_row("# of Partitions", str(len(self.Partitions)))
        self._display.add_row("# of Columns", str(len(self.Columns)))
        self._display.add_row(
            "# of Measures", str(len(self.Measures)), end_section=True
        )
        self._display.add_row("Description", self._object.Description, end_section=True)
        self._display.add_row("DataCategory", str(self._object.DataCategory))
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("IsPrivate", str(self._object.IsPrivate))
        self._display.add_row(
            "ModifiedTime",
            ticks_to_datetime(self._object.ModifiedTime.Ticks).strftime(
                "%m/%d/%Y, %H:%M:%S"
            ),
        )

    def row_count(self) -> int:
        """Method to return count of rows.

        Simple Dax Query: `EVALUATE {COUNTROWS('Table Name')}`.

        Returns:
            int: Number of rows using `COUNTROWS`.

        Example:
            ```python
            model.Tables['Table Name'].row_count()
            ```
        """
        return self.Model.Adomd.query(f"EVALUATE {{COUNTROWS('{self.Name}')}}")

    def refresh(self, *args, **kwargs) -> pd.DataFrame:
        """Use this to refresh the PyTable.

        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details.

        Example:
            ```python
            model.Tables['Table Name'].refresh()

            model.Tables['Table Name'].refresh(trace = None) # (1)
            ```

            1. You can pass through arguments to `PyRefresh`, like removing trace.
        """
        return self.Model.refresh(self, *args, **kwargs)

    def last_refresh(self) -> datetime:
        """Will query each partition for the last refresh time.

        Then will select the max value to return.

        Returns:
            datetime: Last refresh time in datetime format
        """
        partition_refreshes = [
            partition.last_refresh() for partition in self.Partitions
        ]
        return max(partition_refreshes)

    def related(self):
        """Returns tables with a relationship with the table in question."""
        return self.Model.Relationships.related(self)


class PyTables(PyObjects):
    """Groups together multiple tables.

    You can interact with `PyTables` straight from model.
    You can even filter down with `.find()`.
    """

    def __init__(self, objects) -> None:
        """Init just extends from the main `PyObjects` class."""
        super().__init__(objects)

    def refresh(self, *args, **kwargs):
        """Refreshes all `PyTable`(s) in class."""
        model = self._objects[0].Model
        return model.refresh(self, *args, **kwargs)

    def query_all(self, query_function: str = "COUNTROWS(_)") -> pd.DataFrame:
        """Dynamically query all tables.

        It will replace the `_` with the `query_function` arg
        to build out the query to run.

        Args:
                query_function (str, optional): Dax query is
                        dynamically building a query with the
                        `UNION` & `ROW` DAX Functions. Defaults to 'COUNTROWS(_)'.

        Returns:
                pd.DataFrame: Returns dataframe with results

        Example:
            ```python
            model.Tables.find('fact').query_all() # (1)
            ```

            1. Because `.find()` will return the `PyObjects` you are searching in,
            another `PyTables` is returned, but reduced to just
            the `PyTable`(s) with the 'fact' in the name. Then will
            get the # of rows for each table.
        """
        logger.info("Querying every table in PyTables...")
        logger.debug(f"Function to be run: {query_function}")
        logger.debug("Dynamically creating DAX query...")
        query_str = "EVALUATE UNION(\n"
        for table in self:
            table_name = table.get_Name()
            dax_table_identifier = f"'{table_name}'"
            query_str += f"ROW(\"Table\",\"{table_name}\",\"{query_function}\",\
                {query_function.replace('_',dax_table_identifier)}),\n" # noqa: E231, E261
        query_str = f"{query_str[:-2]})"
        return self[0].Model.query(query_str)

    def find_zero_rows(self) -> "PyTables":
        """Returns PyTables class of tables with zero rows queried.

        Returns:
            PyTables: A subset of the `PyTables` that contains zero rows.
        """
        query_function: str = "COUNTROWS(_)"
        df = self.query_all(query_function)

        table_names = df[df[f"[{query_function}]"].isna()]["[Table]"].to_list()
        logger.debug(f"Found {table_names}")
        tables = [self[name] for name in table_names]
        return self.__class__(tables)

    def last_refresh(self, group_partition: bool = True) -> pd.DataFrame:
        """Returns `pd.DataFrame` of tables with their latest refresh time.

        Optional 'group_partition' variable, default is True.
        If False an extra column will be include to
        have the last refresh time to the grain of the partition
        Example to add to model
        `model.Create_Table(p.Table_Last_Refresh_Times(model),'RefreshTimes')`.

        Args:
            group_partition (bool, optional): Whether or not you want
                the grain of the dataframe to be by table or by partition.
                Defaults to True.

        Returns:
            pd.DataFrame: pd dataframe with the RefreshedTime property
                If group_partition == True and the table has
                multiple partitions, then df.groupby(by["tables"]).max()
        """
        data = {
            "Tables": [
                partition.Table.Name for table in self for partition in table.Partitions
            ],
            "Partitions": [
                partition.Name for table in self for partition in table.Partitions
            ],
            "RefreshedTime": [
                partition.last_refresh()
                for table in self
                for partition in table.Partitions
            ],
        }
        df = pd.DataFrame(data)
        if group_partition:
            logger.debug("Grouping together to grain of Table")
            return (
                df[["Tables", "RefreshedTime"]]
                .groupby(by=["Tables"])
                .max()
                .reset_index(drop=False)
            )
        else:
            logger.debug("Returning DF")
            return df
