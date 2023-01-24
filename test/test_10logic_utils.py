"""pytest for the table.py file. Covers the PyTable and PyTables classes.
"""
from test.config import testing_parameters
import pytest
from pytabular import logic_utils
import pandas as pd
import os

sublists = [pytest.param(range(0, 50), x, id=f"Sublist {str(x)}") for x in range(1, 5)]


@pytest.mark.parametrize("lst, n", sublists)
def test_sub_list(lst, n):
    """Tests `get_sub_list()` from `logic_utils.py`."""
    result = logic_utils.get_sub_list(lst, n)
    assert isinstance(result, list)


suffix_list = [
    "helloworld_backup",
    "helloworld_testing",
    "helloworld_suffix",
    "nosuffix",
]


@pytest.mark.parametrize(
    "file_name, suffix",
    [
        pytest.param(
            suffix, suffix[suffix.find("_") + 1 :], id=suffix[suffix.find("_") + 1 :]
        )
        for suffix in suffix_list
    ],
)
def test_remove_suffix(file_name, suffix):
    result = logic_utils.remove_suffix(file_name, suffix)
    assert suffix not in result


dfs = [
    pytest.param(pd.DataFrame({"column_1": [0, 1, 2, 3, 4, 5]}), id="DataFrame1"),
    pytest.param(pd.DataFrame({"column_1": ["one", "two", "three"]}), id="DataFrame2"),
]


@pytest.mark.parametrize("df", dfs)
def test_dataframe_to_dict(df):
    assert isinstance(logic_utils.dataframe_to_dict(df), list)


@pytest.mark.parametrize("model", testing_parameters)
def test_dict_to_markdown_table(model):
    dependencies = [measure.get_dependencies() for measure in model.Measures]
    columns = ["Referenced Object Type", "Referenced Table", "Referenced Object"]
    result = logic_utils.dict_to_markdown_table(dependencies, columns)
    assert isinstance(result, str)


def test_remove_dir():
    dir = "testing_to_be_deleted"
    os.makedirs(dir)
    remove = f"{os.getcwd()}\\{dir}"
    logic_utils.remove_folder_and_contents(remove)
    assert dir not in os.listdir()


def test_remove_file():
    file_to_delete = "testing_to_be_deleted.txt"
    with open(file_to_delete, "w") as f:
        f.write("Delete this file...")
    logic_utils.remove_file(f"{os.getcwd()}\\{file_to_delete}")
    assert file_to_delete not in os.listdir()
