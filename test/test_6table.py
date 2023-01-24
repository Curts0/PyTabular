"""pytest for the table.py file. Covers the PyTable and PyTables classes.
"""
from test.config import testing_parameters, testingtablename
import pytest
import pandas as pd
from datetime import datetime


@pytest.mark.parametrize("model", testing_parameters)
def test_row_count(model):
    """Tests for `Row_Count()` of PyTable class."""
    assert model.Tables[testingtablename].Row_Count() > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh(model):
    """Tests for `Refresh()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].Refresh(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh(model):
    """Tests for `Last_Refresh()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].Last_Refresh(), datetime)


@pytest.mark.parametrize("model", testing_parameters)
def test_related(model):
    """Tests for `Related()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].Related(), type(model.Tables))


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh_pytables(model):
    """Tests for `Refresh()` of PyTables class."""
    assert isinstance(model.Tables.Find(testingtablename).Refresh(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_query_all_pytables(model):
    """Tests for `Query_All()` of PyTables class."""
    assert isinstance(model.Tables.Query_All(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_find_zero_rows_pytables(model):
    """Tests for `Find_Zero_Rows()` of PyTables class."""
    assert isinstance(model.Tables.Find_Zero_Rows(), type(model.Tables))


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh_pytables_true(model):
    """Tests group_partition=True for `Last_Refresh()` of PyTables class."""
    assert isinstance(model.Tables.Last_Refresh(group_partition=True), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh_pytables_false(model):
    """Tests group_partition=False for `Last_Refresh()` of PyTables class."""
    assert isinstance(model.Tables.Last_Refresh(group_partition=False), pd.DataFrame)
