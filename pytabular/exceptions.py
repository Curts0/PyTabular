"""Exceptions raised by PyTabular."""


class PyTabularError(Exception):
    """Base exception for the package."""


class OptionalDependencyError(PyTabularError, ImportError):
    """An optional feature dependency is not installed."""


class RuntimeLoadError(PyTabularError):
    """The .NET runtime or Analysis Services assemblies could not be loaded."""


class ModelSourceError(PyTabularError):
    """A semantic-model source cannot be located or loaded."""


class ModelValidationError(PyTabularError):
    """A semantic model failed validation."""


class LiveConnectionRequiredError(PyTabularError):
    """An operation requires a live XMLA connection."""
