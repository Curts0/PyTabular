"""Public ``Tabular`` facade for live XMLA and offline TMDL models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytabular.results import ModelCapabilities, ModelDiff, SaveResult, ValidationReport
from pytabular.sources import TmdlSource, diff_sources


class _OfflineTabular:
    """A ``Tabular`` model backed by a local TMDL definition."""

    def __init__(self, source: TmdlSource, *, auto_save: bool = True) -> None:
        self._source = source
        self.auto_save = auto_save
        self.Database = source.database
        self.Model = source.model
        self.CompatibilityLevel = int(getattr(self.Database, "CompatibilityLevel", 0))
        self.reload_model_info()

    def reload_model_info(self) -> bool:
        """Refresh collection aliases from the underlying TOM model."""
        collections = {
            "Tables": ("Tables", "tables"),
            "Relationships": ("Relationships", "relationships"),
            "Cultures": ("Cultures", "cultures"),
            "Expressions": ("Expressions", "expressions"),
            "DataSources": ("DataSources", "data_sources"),
            "Functions": ("Functions", "functions"),
        }
        for public_name, (tom_name, pep8_name) in collections.items():
            if hasattr(self.Model, tom_name):
                value = getattr(self.Model, tom_name)
                setattr(self, public_name, value)
                setattr(self, pep8_name, value)

        tables = getattr(self, "Tables", ())
        self.Partitions = [
            partition
            for table in tables
            for partition in getattr(table, "Partitions", ())
        ]
        self.Columns = [
            column for table in tables for column in getattr(table, "Columns", ())
        ]
        self.Measures = [
            measure for table in tables for measure in getattr(table, "Measures", ())
        ]
        self.partitions = self.Partitions
        self.columns = self.Columns
        self.measures = self.Measures
        return True

    @property
    def capabilities(self) -> ModelCapabilities:
        """Return source and compatibility capabilities."""
        return ModelCapabilities(
            compatibility_level=self.CompatibilityLevel,
            source_kind="tmdl",
            live=False,
        )

    def save_changes(self) -> SaveResult:
        """Persist the in-memory TOM database to its TMDL source."""
        result = self._source.save()
        self.reload_model_info()
        return result

    def save_tmdl(self, path: str | Path | None = None) -> SaveResult:
        """Save the model as a TMDL folder."""
        return self._source.save(path)

    def validate(self) -> ValidationReport:
        """Validate the model with TOM."""
        return self._source.validate()

    def diff(self, other: _OfflineTabular) -> ModelDiff:
        """Compare this model with another file-backed model."""
        if not isinstance(other, _OfflineTabular):
            raise TypeError("TMDL diff requires another model loaded with from_tmdl().")
        return diff_sources(self._source, other._source)

    def disconnect(self) -> None:
        """Match the live-model lifecycle API."""

    def __enter__(self) -> _OfflineTabular:
        return self

    def __exit__(self, *_: Any) -> None:
        self.disconnect()


class Tabular:
    """Open a live XMLA model or construct an offline TMDL model.

    ``Tabular(connection_string)`` remains the legacy live entry point.
    """

    def __new__(cls, connection_str: str):
        if cls is not Tabular:
            return super().__new__(cls)
        try:
            from pytabular._legacy import Tabular as LiveTabular
        except ModuleNotFoundError as error:
            if error.name in {"pandas", "rich", "xmltodict"}:
                from pytabular.exceptions import OptionalDependencyError

                raise OptionalDependencyError(
                    "Live XMLA models require the query extra. "
                    "Install 'python-tabular[query]'."
                ) from error
            raise

        return LiveTabular(connection_str)

    @classmethod
    def connect(cls, connection_str: str):
        """Connect to a live XMLA model."""
        return cls(connection_str)

    @classmethod
    def from_tmdl(
        cls,
        path: str | Path,
        *,
        auto_save: bool = True,
    ) -> _OfflineTabular:
        """Load an offline TMDL definition."""
        return _OfflineTabular(TmdlSource.open(path), auto_save=auto_save)

    @classmethod
    def from_pbip(
        cls,
        path: str | Path,
        *,
        auto_save: bool = True,
    ) -> _OfflineTabular:
        """Load the semantic-model definition referenced by a PBIP project."""
        return cls.from_tmdl(path, auto_save=auto_save)
