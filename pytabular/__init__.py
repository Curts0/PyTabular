"""Python tools for tabular semantic models.

The package intentionally performs no CLR setup, logging configuration, model
discovery, or network access during import. Optional features are loaded only
when their public attributes are requested.
"""

from __future__ import annotations

import logging
from importlib import import_module
from typing import Any

__version__ = "0.6.0a1"

logger = logging.getLogger("PyTabular")
logger.addHandler(logging.NullHandler())

_LAZY_EXPORTS = {
    "Tabular": ("pytabular.pytabular", "Tabular"),
    "Tmdl": ("pytabular.tmdl", "Tmdl"),
    "Connection": ("pytabular.query", "Connection"),
    "BaseTrace": ("pytabular.tabular_tracing", "BaseTrace"),
    "RefreshTrace": ("pytabular.tabular_tracing", "RefreshTrace"),
    "QueryMonitor": ("pytabular.tabular_tracing", "QueryMonitor"),
    "TabularEditor": ("pytabular.tabular_editor", "TabularEditor"),
    "BPA": ("pytabular.best_practice_analyzer", "BPA"),
    "ModelDocumenter": ("pytabular.document", "ModelDocumenter"),
    "find_local_pbi_instances": (
        "pytabular.pbi_helper",
        "find_local_pbi_instances",
    ),
}

__all__ = [
    "Tabular",
    "Tmdl",
    "Connection",
    "BaseTrace",
    "RefreshTrace",
    "QueryMonitor",
    "TabularEditor",
    "BPA",
    "ModelDocumenter",
    "find_local_pbi_instances",
    "__version__",
    "logger",
]


def __getattr__(name: str) -> Any:
    """Load optional public features on first use."""
    try:
        module_name, attribute = _LAZY_EXPORTS[name]
    except KeyError as error:
        raise AttributeError(f"module 'pytabular' has no attribute {name!r}") from error

    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Return lazy exports for interactive discovery."""
    return sorted(set(globals()) | set(__all__))
