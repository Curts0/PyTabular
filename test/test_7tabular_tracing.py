"""pytest for the table.py file. Covers the PyTable and PyTables classes."""
from test.config import testing_parameters, testingtablename
import pytest
import pytabular as p
from test.conftest import TestStorage


@pytest.mark.parametrize("model", testing_parameters)
def test_disconnect_for_trace(model):
    """Tests `disconnect()` from `Tabular` class."""
    model.disconnect()
    assert model.Server.Connected is False


@pytest.mark.parametrize("model", testing_parameters)
def test_reconnect_update(model):
    """This will test the `reconnect()`.

    Gets called in `update()` of the `Base_Trace` class.
    """
    model.disconnect()
    model.Tables[testingtablename].refresh()
    assert model.Server.Connected is True


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_start(model):
    """This will test the `QueryMonitor` trace and `start()` it."""
    query_trace = p.QueryMonitor(model)
    query_trace.start()
    TestStorage.query_trace = query_trace
    assert TestStorage.query_trace.Trace.IsStarted


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_stop(model):
    """Tests `stop()` of `QueryMonitor` trace."""
    TestStorage.query_trace.stop()
    assert TestStorage.query_trace.Trace.IsStarted is False


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_drop(model):
    """Tests `drop()` of `QueryMonitor` trace."""
    assert TestStorage.query_trace.drop() is None
