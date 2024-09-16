"""Sanity pytests.

Does 1 actually equal 1?
Or am I crazy person about to descend into madness.
"""

import pytest
from Microsoft.AnalysisServices.Tabular import Database
from test.config import testing_parameters


@pytest.mark.parametrize("model", testing_parameters)
def test_sanity_check(model):
    """Just in case... I might be crazy."""
    assert 1 == 1


@pytest.mark.parametrize("model", testing_parameters)
def test_connection(model):
    """Does a quick check on connection to `Tabular()` class."""
    assert model.Server.Connected


@pytest.mark.parametrize("model", testing_parameters)
def test_database(model):
    """Tests that `model.Database` is actually a Database."""
    assert isinstance(model.Database, Database)
