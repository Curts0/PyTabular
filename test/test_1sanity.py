"""Sanity pytests.

Does 1 actually equal 1?
Or am I crazy person about to descend into madness.
"""

import pytest
from Microsoft.AnalysisServices.Tabular import Database
from test.config import testing_parameters


def test_sanity_check():
    """Just in case... I might be crazy."""
    assert 1 == 1


def test_connection(model):
    """Does a quick check on connection to `Tabular()` class."""
    assert model.Server.Connected


def test_database(model):
    """Tests that `model.Database` is actually a Database."""
    assert isinstance(model.Database, Database)
