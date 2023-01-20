"""pytest for the table.py file. Covers the PyTable and PyTables classes.
"""
from test.config import testing_parameters, testingtablename
import pytest
import pytabular as p
from test.conftest import testing_storage


@pytest.mark.parametrize("model", testing_parameters)
def test_disconnect_for_trace(model):
    """Tests `Disconnect()` from `Tabular` class."""
    model.Disconnect()
    assert model.Server.Connected is False


@pytest.mark.parametrize("model", testing_parameters)
def test_reconnect_update(model):
    """This will test the `Reconnect()` gets called in `Update()`
    of the `Base_Trace` class.
    """
    model.Disconnect()
    model.Tables[testingtablename].Refresh()
    assert model.Server.Connected is True


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_start(model):
    """This will test the `Query_Monitor` trace and `Start()` it."""
    query_trace = p.Query_Monitor(model)
    query_trace.Start()
    testing_storage.query_trace = query_trace
    assert testing_storage.query_trace.Trace.IsStarted


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_stop(model):
    """Tests `Stop()` of `Query_Monitor` trace."""
    testing_storage.query_trace.Stop()
    assert testing_storage.query_trace.Trace.IsStarted is False


@pytest.mark.parametrize("model", testing_parameters)
def test_query_monitor_drop(model):
    """Tests `Drop()` of `Query_Monitor` trace."""
    assert testing_storage.query_trace.Drop() is None
