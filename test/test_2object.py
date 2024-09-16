"""pytest for the table.py file. Covers the PyTable and PyTables classes."""

from test.config import testing_parameters
import pytest
from pytabular import Tabular


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_model(model):
    """Tests successful `__rich_repr()` `on Tabular()` class."""
    try:
        model.__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_table(model):
    """Tests successful `__rich_repr()` `on PyTable()` class."""
    try:
        model.Tables[0].__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_tables(model):
    """Tests successful `__rich_repr()` `on PyTables()` class."""
    try:
        model.Tables.__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_column(model):
    """Tests successful `__rich_repr()` `on PyColumn()` class."""
    try:
        model.Columns[0].__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_columns(model):
    """Tests successful `__rich_repr()` `on PyColumns()` class."""
    try:
        model.Columns.__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_partition(model):
    """Tests successful `__rich_repr()` `on PyPartition()` class."""
    try:
        model.Partitions[0].__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_partitions(model):
    """Tests successful `__rich_repr()` `on PyPartitions()` class."""
    try:
        model.Partitions.__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_measure(model):
    """Tests successful `__rich_repr()` `on PyMeasure()` class."""
    try:
        model.Measures[0].__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_rich_repr_measures(model):
    """Tests successful `__rich_repr()` `on PyMeasures()` class."""
    try:
        model.Measures.__rich_repr__()
    except Exception:
        pytest.fail("__rich_repr__() failed")


@pytest.mark.parametrize("model", testing_parameters)
def test_get_attr(model):
    """Tests custom get attribute from `PyObject` class."""
    assert isinstance(model.Tables[0].Model, Tabular)


@pytest.mark.parametrize("model", testing_parameters)
def test_iadd_tables(model):
    """Tests `__iadd__()` with `PyTables()`."""
    a = model.Tables.find("Sales")
    b = model.Tables.find("Date")
    a += b
    assert len(a.find("Date")) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_iadd_table(model):
    """Tests `__iadd__()` with a `PyTable()`."""
    a = model.Tables.find("Sales")
    b = model.Tables.find("Date")[0]
    a += b
    assert len(a.find("Date")) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_find_measure(model):
    """Tests `find()` with a `PyMeasure()`."""
    a = model.Measures[0].Name
    b = model.Measures.find(a)
    assert len(b) > 0
