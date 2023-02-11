"""pytest for the table.py file. Covers the PyTable and PyTables classes."""
from test.config import testing_parameters, testingtablename
import pytest
import pandas as pd
from datetime import datetime


@pytest.mark.parametrize("model", testing_parameters)
def test_row_count(model):
    """Tests for `Row_Count()` of PyTable class."""
    assert model.Tables[testingtablename].row_count() > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh(model):
    """Tests for `Refresh()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].refresh(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh(model):
    """Tests for `Last_Refresh()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].last_refresh(), datetime)


@pytest.mark.parametrize("model", testing_parameters)
def test_related(model):
    """Tests for `Related()` of PyTable class."""
    assert isinstance(model.Tables[testingtablename].related(), type(model.Tables))


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh_pytables(model):
    """Tests for `Refresh()` of PyTables class."""
    assert isinstance(model.Tables.find(testingtablename).refresh(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_query_all_pytables(model):
    """Tests for `Query_All()` of PyTables class."""
    assert isinstance(model.Tables.query_all(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_find_zero_rows_pytables(model):
    """Tests for `Find_Zero_Rows()` of PyTables class."""
    assert isinstance(model.Tables.find_zero_rows(), type(model.Tables))


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh_pytables_true(model):
    """Tests group_partition=True for `Last_Refresh()` of PyTables class."""
    assert isinstance(model.Tables.last_refresh(group_partition=True), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh_pytables_false(model):
    """Tests group_partition=False for `Last_Refresh()` of PyTables class."""
    assert isinstance(model.Tables.last_refresh(group_partition=False), pd.DataFrame)
