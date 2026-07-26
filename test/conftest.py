"""Safety gate for the legacy Power BI Desktop integration suite."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

_ENABLED = os.getenv("PYTABULAR_RUN_LEGACY_DESKTOP_TESTS") == "1"


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    """Never import legacy live tests unless they were explicitly enabled."""
    return not _ENABLED and collection_path.name.startswith("test_")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Label every enabled legacy test as a Desktop integration test."""
    marker = pytest.mark.desktop
    for item in items:
        if "\\test\\" in str(item.path) or "/test/" in str(item.path):
            item.add_marker(marker)
