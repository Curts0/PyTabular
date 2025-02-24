"""`query.py` houses a custom `Connection` class that uses the .Net AdomdConnection.

`Connection` is created automatically when connecting to your model.

Example:
    ```python title="query from model"
    import pytabular as p
    model = p.Tabular(CONNECTION_STR)
    model.query("EVALUATE {1}")
    ```

    ```python title="pass an effective user"
    model.query(
        "EVALUATE {1}",
        effective_user = "user@company.com"
    )
    ```
"""

import logging
import os
from typing import Union
from pytabular.logic_utils import get_value_to_df
import pandas as pd
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection


logger = logging.getLogger("PyTabular")


class Connection(AdomdConnection):
    """Connection class creates an AdomdConnection.

    Mainly used for the `query()` method. The `query()`
    method in the Tabular class is just a wrapper for this class.
    But you can pass through your `effective_user` more efficiently,
    so use that instead.
    """

    def __init__(self, server, effective_user=None) -> None:
        """Init creates the connection.

        Args:
            server (Server): The server that you are connecting to.
            effective_user (str, optional): Pass through an effective user
                to query as somebody else. Defaults to None.
        """
        super().__init__()
        if server.ConnectionInfo.Password is None:
            connection_string = server.ConnectionString
        else:
            connection_string = (
                f"{server.ConnectionString};Password='{server.ConnectionInfo.Password}'"
            )
        logger.debug(f"ADOMD Connection: {connection_string}")
        if effective_user is not None:
            connection_string += f";EffectiveUserName={effective_user}"
        self.ConnectionString = connection_string

    def query(self, query_str: str) -> Union[pd.DataFrame, str, int]:
        """Executes query on Model and returns results in Pandas DataFrame.

        Iterates through results of `AdomdCommmand().ExecuteReader()`
        in the .Net library. If result is a single value, it will
        return that single value instead of DataFrame.

        Args:
            query_str (str): Dax Query. Note, needs full syntax
                (ex: `EVALUATE`). See [DAX](https://docs.microsoft.com/en-us/dax/dax-queries).
                Will check if query string is a file.
                If it is, then it will perform a query
                on whatever is read from the file.
                It is also possible to query DMV.
                For example.
                `query("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES")`.

        Returns:
            pd.DataFrame: Returns dataframe with results.
        """
        try:
            is_file = os.path.isfile(query_str)
        except Exception:
            is_file = False

        if is_file:
            logger.debug(
                f"File path detected, reading file... -> {query_str}",
            )
            with open(query_str, "r") as file:
                query_str = str(file.read())

        if str(self.get_State()) != "Open":
            # Works for now, need to update to handle different types of conneciton properties
            # https://learn.microsoft.com/en-us/dotnet/api/system.data.connectionstate?view=net-7.0
            logger.info("Checking initial Adomd Connection...")
            self.Open()
            logger.info(f"Connected! Session ID - {self.SessionID}")

        logger.debug("Querying Model...")
        logger.debug(query_str)
        query = AdomdCommand(query_str, self).ExecuteReader()
        column_headers = [
            (index, query.GetName(index)) for index in range(0, query.FieldCount)
        ]
        results = list()
        while query.Read():
            results.append(
                [
                    get_value_to_df(query, index)
                    for index in range(0, len(column_headers))
                ]
            )

        query.Close()
        logger.debug("Data retrieved... reading...")
        df = pd.DataFrame(results, columns=[value for _, value in column_headers])
        if len(df) == 1 and len(df.columns) == 1:
            return df.iloc[0][df.columns[0]]
        return df
