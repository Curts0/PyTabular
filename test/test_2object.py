"""pytest for the table.py file. Covers the PyTable and PyTables classes.
"""
from test.config import testing_parameters
import pytest
from pytabular import logic_utils, Tabular
import pandas as pd
import os

@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_model(model):
    try:
        model.__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_table(model):
    try:
        model.Tables[0].__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")



@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_tables(model):
    try:
        model.Tables.__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")



@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_column(model):
    try:
        model.Columns[0].__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")
        


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_columns(model):
    try:
        model.Columns.__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_partition(model):
    try:
        model.Partitions[0].__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")



@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_partitions(model):
    try:
        model.Partitions.__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_measure(model):
    try:
        model.Measures[0].__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_measures(model):
    try:
        model.Measures.__rich_repr__()
    except:
        pytest.fail("__rich_repr__() failed")

#TODO need to get this to have coverage for full getattr
@pytest.mark.parametrize("model", testing_parameters)
def test_get_attr(model):
    assert isinstance(model.Tables[0].Model, Tabular)

@pytest.mark.parametrize("model", testing_parameters)
def test_iadd_tables(model):
    a = model.Tables.Find('Sales')
    b = model.Tables.Find('Date')
    a += b
    assert len(a.Find('Date')) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_iadd_table(model):
    a = model.Tables.Find('Sales')
    b = model.Tables.Find('Date')[0]
    a += b
    assert len(a.Find('Date')) > 0