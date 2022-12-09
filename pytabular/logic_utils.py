import logging
import datetime
import os
from typing import Dict, List
import pandas as pd
from Microsoft.AnalysisServices.Tabular import DataType

logger = logging.getLogger("PyTabular")


def ticks_to_datetime(ticks: int) -> datetime.datetime:
    """Converts a C# System DateTime Tick into a Python DateTime

    Args:
            ticks (int): [C# DateTime Tick](https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0)

    Returns:
            datetime.datetime: [datetime.datetime](https://docs.python.org/3/library/datetime.html)
    """
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=ticks // 10)


def pandas_datatype_to_tabular_datatype(df: pd.DataFrame) -> Dict:
    """WiP takes dataframe columns and gets respective tabular column datatype.  ([NumPy Datatypes](https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html) and [Tabular Datatypes](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datatype?view=analysisservices-dotnet))

    Args:
            df (pd.DataFrame): Pandas DataFrame

    Returns:
            Dict: EX {'col1': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9700>, 'col2': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC8840>, 'col3': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9800>}
    """
    logger.info("Getting DF Column Dtypes to Tabular Dtypes...")
    tabular_datatype_mapping_key = {
        "b": DataType.Boolean,
        "i": DataType.Int64,
        "u": DataType.Int64,
        "f": DataType.Double,
        "c": DataType.Double,
        "m": DataType.DateTime,
        "M": DataType.DateTime,
        "O": DataType.String,
        "S": DataType.String,
        "U": DataType.String,
        "V": DataType.String,
    }
    return {
        column: tabular_datatype_mapping_key[df[column].dtype.kind]
        for column in df.columns
    }


def pd_dataframe_to_dax_expression(
    df: pd.DataFrame = pd.DataFrame(data={"col1": [1.0, 2.0], "col2": [3, 4]})
) -> str:
    """
    This will take a pandas dataframe and convert to a dax expression
    For example this DF:
            col1  col2
    0   1     3
    1   2     4

    |
    |
    V

    Will convert to this expression string:
    DEFINE
            TABLE tablename = { ( 1, 3 ), ( 2, 4 ) }

    EVALUATE
    SELECTCOLUMNS(
            tablename,
            "col1", tablename[Value1],
            "col2", tablename[Value2]
    )
    """

    def dax_tableconstructor_rows_expression_generator(
        list_of_strings: list[str],
    ) -> str:
        """
        Converts list[str] to dax table rows for example ['one','two'] -> '('one','two')'
        """
        return

    return True


def pd_dataframe_to_m_expression(df: pd.DataFrame) -> str:
    """This will take a pandas dataframe and convert to an m expression
    For example this DF:
       col1  col2
    0   1     3
    1   2     4

    |
    |
    V

    Will convert to this expression string:
    let
    Source=#table({"col1","col2"},
    {
    {"1","3"},{"2","4"}
    })
    in
    Source

    Args:
            df (pd.DataFrame): Pandas DataFrame

    Returns:
            str: Currently only returning string values in your tabular model.
    """

    def m_list_expression_generator(list_of_strings: List[str]) -> str:
        """
        Takes a python list of strings and converts to power query m expression list format...
        Ex: ["item1","item2","item3"] --> {"item1","item2","item3"}
        Codepoint reference --> \u007b == { and \u007d == }
        """
        string_components = ",".join(
            [f'"{string_value}"' for string_value in list_of_strings]
        )
        return f"\u007b{string_components}\u007d"

    logger.debug(f"Executing m_list_generator()... for {df.columns}")
    columns = m_list_expression_generator(df.columns)
    expression_str = f"let\nSource=#table({columns},\n"
    logger.debug(
        f"Iterating through rows to build expression... df has {len(df)} rows..."
    )
    expression_list_rows = []
    for index, row in df.iterrows():
        expression_list_rows += [m_list_expression_generator(row.to_list())]
    expression_str += f"\u007b\n{','.join(expression_list_rows)}\n\u007d)\nin\nSource"
    return expression_str


def remove_folder_and_contents(folder_location):
    """Internal used in tabular_editor.py and best_practice_analyzer.py.

    Args:
            folder_location (str): Folder path to remove directory and contents.
    """
    import shutil

    if os.path.exists(folder_location):
        logger.info(f"Removing Dir and Contents -> {folder_location}")
        shutil.rmtree(folder_location)


def remove_suffix(input_string, suffix):
    """Adding for >3.9 compatiblity. [Stackoverflow Answer](https://stackoverflow.com/questions/66683630/removesuffix-returns-error-str-object-has-no-attribute-removesuffix)

    Args:
            input_string (str): input string to remove suffix from
            suffix (str): suffix to be removed

    Returns:
            str: input_str with suffix removed
    """
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return input_string


def sql_wrap_count_around_query(original_query: str) -> str:
    """Simple string formating to get the total row count of a sql query.

    Args:
            original_query (str): Regular sql query to get count of.

    Returns:
            str: f"SELECT COUNT(1) FROM ({original_query}) temp_table"
    """
    return f"SELECT COUNT(1) FROM ({original_query}) temp_table"


def get_sub_list(lst: list, n: int) -> list:
    """Nest list by n amount...
    `get_sub_list([1,2,3,4,5,6],2) == [[1,2],[3,4],[5,6]]`

    Args:
        lst (list): List to nest.
        n (int): Amount to nest list.

    Returns:
        list: Nested list.
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]
