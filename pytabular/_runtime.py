"""Lazy Pythonnet and Analysis Services runtime loading."""

from __future__ import annotations

import threading
from importlib import import_module
from pathlib import Path
from types import ModuleType

from pytabular.exceptions import OptionalDependencyError, RuntimeLoadError

_LOCK = threading.Lock()
_TOM: ModuleType | None = None
_ADOMD: ModuleType | None = None


def _assembly_directory() -> Path:
    package_root = Path(__file__).resolve().parent
    generated = package_root / "_vendor"
    legacy = package_root / "dll"
    if (generated / "Microsoft.AnalysisServices.Tabular.dll").is_file():
        return generated
    if (legacy / "Microsoft.AnalysisServices.Tabular.dll").is_file():
        return legacy
    raise RuntimeLoadError(
        "Analysis Services assemblies are unavailable. Install a PyPI wheel or "
        "run tools/restore-runtime.ps1 from a source checkout."
    )


def _load_clr() -> None:
    try:
        from pythonnet import load
    except ImportError as error:
        raise OptionalDependencyError(
            "TOM support requires pythonnet. Install 'python-tabular'."
        ) from error

    try:
        load("coreclr")
    except RuntimeError as error:
        # Pythonnet raises when a runtime has already been initialized. In that
        # case importing clr below is the authoritative compatibility check.
        if "already" not in str(error).lower():
            raise RuntimeLoadError("Unable to initialize .NET Core.") from error

    try:
        import clr
    except ImportError as error:
        raise RuntimeLoadError(
            "Pythonnet loaded but the clr module is unavailable."
        ) from error

    assembly_dir = _assembly_directory()
    for name in (
        "Microsoft.AnalysisServices.Core",
        "Microsoft.AnalysisServices.Tabular.Json",
        "Microsoft.AnalysisServices.Tabular",
        "Microsoft.AnalysisServices",
        "Microsoft.AnalysisServices.AdomdClient",
    ):
        path = assembly_dir / f"{name}.dll"
        if path.is_file():
            clr.AddReference(str(path))


def load_tom() -> ModuleType:
    """Load and return ``Microsoft.AnalysisServices.Tabular``."""
    global _TOM
    if _TOM is None:
        with _LOCK:
            if _TOM is None:
                _load_clr()
                try:
                    _TOM = import_module("Microsoft.AnalysisServices.Tabular")
                except ImportError as error:
                    raise RuntimeLoadError(
                        "Unable to import the TOM assembly."
                    ) from error
    return _TOM


def load_adomd() -> ModuleType:
    """Load and return ``Microsoft.AnalysisServices.AdomdClient``."""
    global _ADOMD
    if _ADOMD is None:
        with _LOCK:
            if _ADOMD is None:
                _load_clr()
                try:
                    _ADOMD = import_module("Microsoft.AnalysisServices.AdomdClient")
                except ImportError as error:
                    raise RuntimeLoadError(
                        "Unable to import the ADOMD assembly."
                    ) from error
    return _ADOMD
