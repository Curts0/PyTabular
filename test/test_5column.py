"""pytest for the column.py file. Covers the PyColumn and PyColumns classes."""

from test.config import testing_parameters, testingtablename
import pytest
import pandas as pd
from numpy import int64


@pytest.mark.parametrize("model", testing_parameters)
def test_values(model):
    """Tests for `Values()` of PyColumn class."""
    vals = model.Tables[testingtablename].Columns[1].values()
    assert isinstance(vals, pd.DataFrame) or isinstance(vals, int)


@pytest.mark.parametrize("model", testing_parameters)
def test_distinct_count_no_blank(model):
    """Tests No_Blank=True for `Distinct_Count()` of PyColumn class."""
    vals = model.Tables[testingtablename].Columns[1].distinct_count(no_blank=True)
    assert isinstance(vals, int64)


@pytest.mark.parametrize("model", testing_parameters)
def test_distinct_count_blank(model):
    """Tests No_Blank=False for `Distinct_Count()` of PyColumn class."""
    vals = model.Tables[testingtablename].Columns[1].distinct_count(no_blank=False)
    assert isinstance(vals, int64)


@pytest.mark.parametrize("model", testing_parameters)
def test_get_sample_values(model):
    """Tests for `get_sample_values()` of PyColumn class."""
    sample_vals = model.Tables[testingtablename].Columns[1].get_sample_values()
    assert isinstance(sample_vals, pd.DataFrame) or isinstance(sample_vals, int)


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_column(model):
    """Tests `Query_All()` of PyColumns class."""
    assert isinstance(model.Tables[testingtablename].Columns.query_all(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_dependencies(model):
    """Tests execution of `PyColumn().get_dependencies()`."""
    df = model.Tables[0].Columns[1].get_dependencies()
    assert isinstance(df, pd.DataFrame)
