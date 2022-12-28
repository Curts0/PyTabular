import pytest
from Microsoft.AnalysisServices.Tabular import Database
from test.config import testing_parameters


@pytest.mark.parametrize("model", testing_parameters)
def test_sanity_check(model):
    """Just in case... I might be crazy"""
    assert 1 == 1


@pytest.mark.parametrize("model", testing_parameters)
def test_connection(model):
    """
    Does a quick check to the Tabular Class
    To ensure that it can connnect
    """
    assert model.Server.Connected


@pytest.mark.parametrize("model", testing_parameters)
def test_database(model):
    assert isinstance(model.Database, Database)
