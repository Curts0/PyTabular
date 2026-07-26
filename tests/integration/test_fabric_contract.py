"""Read-only live XMLA contract test."""

from __future__ import annotations

import os

import pytest


@pytest.mark.fabric
def test_connect_to_explicit_fabric_model() -> None:
    connection_string = os.getenv("PYTABULAR_TEST_CONNECTION_STRING")
    if not connection_string:
        pytest.skip("PYTABULAR_TEST_CONNECTION_STRING is not configured")

    from pytabular import Tabular

    model = Tabular.connect(connection_string)
    try:
        assert model.Server.Connected
    finally:
        model.disconnect()
