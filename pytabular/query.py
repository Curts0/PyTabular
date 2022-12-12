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

    def __init__(self, Server, Effective_User=None) -> None:
        super().__init__()
        connection_string = (
            f"{Server.ConnectionString}Password='{Server.ConnectionInfo.Password}'"
        )
        if Effective_User is not None:
            connection_string += f";EffectiveUserName={Effective_User}"
        self.ConnectionString = connection_string

    def Query(self, Query_Str: str) -> Union[pd.DataFrame, str, int]:
        """Executes Query on Model and Returns Results in Pandas DataFrame

        Args:
                Query_Str (str): Dax Query. Note, needs full syntax (ex: EVALUATE). See (DAX Queries)[https://docs.microsoft.com/en-us/dax/dax-queries].
                Will check if query string is a file. If it is, then it will perform a query on whatever is read from the file.
                It is also possible to query DMV. For example. Query("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"). See (DMVs)[https://docs.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions]

        Returns:
                pd.DataFrame: Returns dataframe with results
        """
        try:
            is_file = os.path.isfile(Query_Str)
        except Exception:
            is_file = False

        if is_file:
            logger.debug(
                f"File path detected, reading file... -> {Query_Str}",
            )
            with open(Query_Str, "r") as file:
                Query_Str = str(file.read())

        if self.State.value__ == 0:
            logger.info("Checking initial Adomd Connection...")
            self.Open()
            logger.info(f"Connected! Session ID - {self.SessionID}")

        logger.debug("Querying Model...")
        logger.debug(Query_Str)
        Query = AdomdCommand(Query_Str, self).ExecuteReader()
        Column_Headers = [
            (index, Query.GetName(index)) for index in range(0, Query.FieldCount)
        ]
        Results = list()
        while Query.Read():
            Results.append(
                [
                    get_value_to_df(Query, index)
                    for index in range(0, len(Column_Headers))
                ]
            )

        Query.Close()
        logger.debug("Data retrieved... reading...")
        df = pd.DataFrame(Results, columns=[value for _, value in Column_Headers])
        if len(df) == 1 and len(df.columns) == 1:
            return df.iloc[0][df.columns[0]]
        return df
