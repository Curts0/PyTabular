from test.config import aas, gen2
import pytest
from Microsoft.AnalysisServices.Tabular import Database

testing_parameters = [pytest.param(aas, id="AAS"), pytest.param(gen2, id="GEN2")]


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
