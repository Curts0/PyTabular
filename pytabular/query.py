"""
`query.py` houses a custom `Connection` class that uses the .Net AdomdConnection.
`Connection` is created automatically when connecting to your model.
"""
import logging
import os
from typing import Union
from logic_utils import get_value_to_df
import pandas as pd
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection


logger = logging.getLogger("PyTabular")


class Connection(AdomdConnection):
    """Subclass for [Adomdclient](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.adomdclient?view=analysisservices-dotnet). With some extra items on top.
    Right now designed for internal use. For example, Query method in the Tabular class is just a wrapper for this class' Query method... So use that instead.

    Args:
        AdomdConnection (_type_): _description_
    """

    def __init__(self, server, effective_user=None) -> None:
        super().__init__()
        if server.ConnectionInfo.Password is None:
            connection_string = server.ConnectionString
        else:
            connection_string = (
                f"{server.ConnectionString}Password='{server.ConnectionInfo.Password}'"
            )
        logger.debug(f"{connection_string}")
        if effective_user is not None:
            connection_string += f";EffectiveUserName={effective_user}"
        self.ConnectionString = connection_string

    def query(self, query_str: str) -> Union[pd.DataFrame, str, int]:
        """Executes Query on Model and Returns results in Pandas DataFrame

        Args:
                query_str (str): Dax Query. Note, needs full syntax (ex: EVALUATE). See (DAX Queries)[https://docs.microsoft.com/en-us/dax/dax-queries].
                Will check if query string is a file. If it is, then it will perform a query on whatever is read from the file.
                It is also possible to query DMV. For example. Query("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"). See (DMVs)[https://docs.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions]

        Returns:
                pd.DataFrame: Returns dataframe with results
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
