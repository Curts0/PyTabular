"""`logic_utils` used to store multiple functions that are used in many different files."""

import logging
import datetime
import os
from typing import Dict, List
import pandas as pd
from Microsoft.AnalysisServices.Tabular import DataType
from Microsoft.AnalysisServices.AdomdClient import AdomdDataReader

logger = logging.getLogger("PyTabular")


def ticks_to_datetime(ticks: int) -> datetime.datetime:
    """Converts a C# system datetime tick into a python datatime.

    Args:
            ticks (int): C# DateTime Tick.

    Returns:
            datetime.datetime: datetime of tick.
    """
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=ticks // 10)


def pandas_datatype_to_tabular_datatype(df: pd.DataFrame) -> Dict:
    """Takes dataframe columns and gets respective tabular column datatype.

    Args:
            df (pd.DataFrame): Pandas DataFrame

    Returns:
            Dict: dictionary with results.

    Example:
        ```
        {
            'col1': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9700>,
            'col2': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC8840>,
            'col3': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9800>
        }
        ```
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


def pd_dataframe_to_m_expression(df: pd.DataFrame) -> str:
    """This will take a pandas dataframe and convert to an m expression.

    Args:
            df (pd.DataFrame): Pandas DataFrame

    Returns:
            str: Currently only returning string values in your tabular model.

    Example:
        ```
        col1  col2
        0   1     3
        1   2     4
        ```
        converts to
        ```
        Source=#table({"col1","col2"},
        {
        {"1","3"},{"2","4"}
        })
        in
        Source
        ```
    """

    def m_list_expression_generator(list_of_strings: List[str]) -> str:
        """Takes a python list of strings and converts to power query m expression list format.

        Ex: `["item1","item2","item3"]` --> `{"item1","item2","item3"}`
        Codepoint reference --> `\u007b` == `{` and `\u007d` == `}`
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
    for _, row in df.iterrows():
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


def remove_file(file_path):
    """Just `os.remove()` but wanted a `logger.info()` with it."""
    logger.info(f"Removing file - {file_path}")
    os.remove(file_path)
    pass


def remove_suffix(input_string, suffix):
    """Adding for <3.9 compatiblity.

    Args:
            input_string (str): input string to remove suffix from.
            suffix (str): suffix to be removed.
    """
    # [Stackoverflow Answer](https://stackoverflow.com/questions/66683630/removesuffix-returns-error-str-object-has-no-attribute-removesuffix)  # noqa: E501
    output = (
        input_string[: -len(suffix)]
        if suffix and input_string.endswith(suffix)
        else input_string
    )
    return output


def get_sub_list(lst: list, n: int) -> list:
    """Nest list by n amount.

    Args:
        lst (list): List to nest.
        n (int): Amount to nest list.

    Returns:
        list: Nested list.
    Example:
        `get_sub_list([1,2,3,4,5,6],2) == [[1,2],[3,4],[5,6]]`
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def get_value_to_df(query: AdomdDataReader, index: int):
    """Gets the values from the AdomdDataReader to convert to python df.

    Lots of room for improvement on this one.

    Args:
        query (AdomdDataReader): The AdomdDataReader .Net object.
        index (int): Index of the value to perform the logic on.
    """
    if (
        query.GetDataTypeName((index)) in ("Decimal")
        and query.GetValue(index) is not None
    ):
        return query.GetValue(index).ToDouble(query.GetValue(index))
    else:
        return query.GetValue(index)


def dataframe_to_dict(df: pd.DataFrame) -> List[dict]:
    """Convert to Dataframe to dictionary and alter columns names with it.

    Will convert the underscores (_) to spaces,
    and all strings are converted to Title Case.

    Args:
        df (pd.DataFrame): Original table that needs to be converted
            to a list with dicts.

    Returns:
        list of dictionaries.
    """
    list_of_dicts = df.to_dict("records")
    return [
        {k.replace("_", " ").title(): v for k, v in dict.items()}
        for dict in list_of_dicts
    ]


def dict_to_markdown_table(list_of_dicts: list, columns_to_include: list = None) -> str:
    """Generate a Markdown table based on a list of dictionaries.

    Args:
        list_of_dicts (list): List of Dictionaries that need to be converted
            to a markdown table.
        columns_to_include (list): Default = None, and all colums are included.
            If a list is supplied, those columns will be included.

    Returns:
        String that will represent a table in Markdown.

    Example:
        ```python
            columns = ['Referenced Object Type', 'Referenced Table', 'Referenced Object']
            dict_to_markdown_table(dependancies, columns)
        ```
        Returns:
        ```
            | Referenced Object Type | Referenced Table | Referenced Object               |
            | ---------------------- | ---------------- | ------------------------------- |
            | TABLE                  | Cases            | Cases                           |
            | COLUMN                 | Cases            | IsClosed                        |
            | CALC_COLUMN            | Cases            | Resolution Time (Working Hours) |
        ```
    """
    keys = set().union(*[set(d.keys()) for d in list_of_dicts])

    if columns_to_include is not None:
        keys = list(keys.intersection(columns_to_include))

    table_header = f"| {' | '.join(map(str, keys))} |"
    table_header_separator = "|-----" * len(keys) + "|"
    markdown_table = [table_header, table_header_separator]

    for row in list_of_dicts:
        table_row = f"| {' | '.join(str(row.get(key, '')) for key in keys)} |"
        markdown_table.append(table_row)
    return "\n".join(markdown_table)
