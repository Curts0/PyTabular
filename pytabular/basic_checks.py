"""
All basic checks will eventually be deprecated for more intuitive methods in the right classes.
For example, instead of calling the function `Return_Zero_Row_Tables(model)`,
call the Find_Zero_Rows() method in the PyTables class.
That way you can dynamically run those methods on a subset of tables,
instead of only on the entire model.
"""
import logging
from typing import List, Union
import pytabular
from logic_utils import ticks_to_datetime
import sys
import pandas as pd
from measure import PyMeasure

logger = logging.getLogger("PyTabular")


def Return_Zero_Row_Tables(model: pytabular.Tabular) -> List[str]:
    """Returns list of table names of those that are returning isna()
    Args:
            model (pytabular.Tabular): Tabular Model
    Returns:
            List[str]: List of table names where DAX COUNTROWS('Table Name') is nan or 0.
    """
    logger.warning(
        "Return_Zero_Row_Tables() will be deprecated. \
        Instead use Zero_Row_Tables() through the PyTables class."
    )
    query_function: str = "COUNTROWS(_)"
    df: pd.DataFrame = model.Tables.Query_All(query_function)
    return df[df[f"[{query_function}]"].isna()]["[Table]"].to_list()


def Table_Last_Refresh_Times(
    model: pytabular.Tabular, group_partition: bool = True
) -> pd.DataFrame:
    """Returns pd.DataFrame of tables with their latest refresh time.
    Optional 'group_partition' variable, default is True.
    If False an extra column will be include to have the last refresh time to the grain of the partition
    Example to add to model model.Create_Table(p.Table_Last_Refresh_Times(model),'RefreshTimes')
    Args:
            model (pytabular.Tabular): Tabular Model
            group_partition (bool, optional): Whether or not you want the grain of the dataframe to be by table or by partition. Defaults to True.
    Returns:
            pd.DataFrame: pd dataframe with the RefreshedTime property: https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition.refreshedtime?view=analysisservices-dotnet#microsoft-analysisservices-tabular-partition-refreshedtime
            If group_partition == True and the table has multiple partitions, then df.groupby(by["tables"]).max()
    """
    logger.info(f"Executing Basic Function {sys._getframe(0).f_code.co_name}")
    logger.warning(
        f"{sys._getframe(0).f_code.co_name} will be deprecated... Use Last_Refresh in PyTables class instead!"
    )

    data = {
        "Tables": [partition.Table.Name for partition in model.Partitions],
        "Partitions": [partition.Name for partition in model.Partitions],
        "RefreshedTime": [
            ticks_to_datetime(partition.RefreshedTime.Ticks).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )[:-3]
            for partition in model.Partitions
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


def BPA_Violations_To_DF(model: pytabular.Tabular, te2: str, bpa: str) -> pd.DataFrame:
    """Runs BPA Analyzer from TE2 and outputs result into a DF.

    Args:
            model (pytabular.Tabular): Tabular Model Class
            te2 (str): TE2 Exe File Path (Can use TE2().EXE_path)
            bpa (str): BPA File Location (Can use BPA().Location)

    Returns:
            pd.DataFrame: Super simple right now. Just splits into two columns.. The object in violation and the rule.
    """
    results = model.Analyze_BPA(te2, bpa)
    data = [
        rule.replace(" violates rule ", "^").replace('"', "").split("^")
        for rule in results
    ]
    columns = ["Object", "Violation"]
    return pd.DataFrame(data, columns=columns)


def Last_X_Interval(
    Model: pytabular.Tabular,
    Measure: Union[str, PyMeasure],
    Column_Name: Union[str, None] = None,
    Date_Column_Identifier: str = "'Date'[DATE_DTE_KEY]",
    Number_Of_Intervals: int = 90,
    Interval: str = "DAY",
) -> pd.DataFrame:
    """Pulls the Last X Interval (Ex Last 90 Days) of a specific measure.

    Args:
            Model (pytabular.Tabular): Tabular Model to perform query on.
            Measure (Union[str,pytabular.pytabular.Measure]): Measure to query. If string, will first check for a measure in the model with that name, otherwise will assume it is a DAX Expression (Ex SUM(FactTable[ColumnValue]) ) and perform that as expression
            Column_Name (Union[str,None], optional): Column Name to be outputted in DataFrame. You can provide your own otherwise will take from the Measure Name. Defaults to "Result".
            Date_Column_Identifier (str, optional): Date column dax identifier. Defaults to "'Date'[DATE_DTE_KEY]".
            Number_Of_Intervals (int, optional): This is used to plug in the variables for [DATESINPERIOD](https://docs.microsoft.com/en-us/dax/datesinperiod-function-dax). Defaults to 90.
            Interval (str, optional): Sames as Number_Of_Intervals. Used to plug in parameters of DAX function [DATESINPERIOD](https://docs.microsoft.com/en-us/dax/datesinperiod-function-dax). Defaults to "DAY". Possible options are "DAY", "MONTH", "QUARTER", and "YEAR"

    Returns:
            pd.DataFrame: Pandas DataFrame of results.
    """
    if isinstance(PyMeasure, str):
        try:
            Measure = [
                measure for measure in Model.Measures if measure.Name == Measure
            ][-1]
            Column_Name = Measure.Name if Column_Name is None else Column_Name
            Expression = f"[{Measure.Name}]"
        except Exception:
            logging.debug("Measure is string but unable to find Measure...")
            Column_Name = "Result" if Column_Name is None else Column_Name
            Expression = Measure
    else:
        Column_Name = Measure.Name if Column_Name is None else Column_Name
        Expression = f"[{Column_Name}]"
    Query_Str = f"""
    EVALUATE
        SUMMARIZECOLUMNS(
        {Date_Column_Identifier},
        KEEPFILTERS( DATESINPERIOD ( {Date_Column_Identifier}, UTCTODAY(), -{Number_Of_Intervals}, {Interval} ) ),
        "{Column_Name}", {Expression}
        )
    """
    logging.info(
        f"Running query for {Column_Name} in the last {Number_Of_Intervals} {Interval}s..."
    )
    return Model.Query(Query_Str)
