"""Typed results shared by file-backed and live models."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


class JsonResult:
    """Mixin for deterministic JSON serialization."""

    def to_dict(self) -> dict[str, Any]:
        """Return this result as plain Python values."""
        return asdict(self)  # pyright: ignore[reportArgumentType]

    def to_json(self, *, indent: int | None = 2) -> str:
        """Return deterministic JSON."""
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True, default=str)


@dataclass(frozen=True)
class ModelCapabilities(JsonResult):
    """Features available for a loaded model."""

    compatibility_level: int
    source_kind: str
    live: bool
    supports_tmdl: bool = True


@dataclass(frozen=True)
class ValidationMessage(JsonResult):
    """One TOM validation message."""

    message: str
    severity: str = "error"
    code: str | None = None
    path: str | None = None


@dataclass(frozen=True)
class ValidationReport(JsonResult):
    """Model validation outcome."""

    valid: bool
    messages: tuple[ValidationMessage, ...] = ()

    def raise_for_errors(self) -> None:
        """Raise when validation found an error."""
        if not self.valid:
            from pytabular.exceptions import ModelValidationError

            details = "; ".join(message.message for message in self.messages)
            raise ModelValidationError(details or "Semantic model validation failed.")


@dataclass(frozen=True)
class ModelDiff(JsonResult):
    """Canonical TMDL file differences between two models."""

    added_files: tuple[str, ...] = ()
    removed_files: tuple[str, ...] = ()
    changed_files: tuple[str, ...] = ()
    patches: dict[str, str] = field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        """Whether the model definitions are equivalent."""
        return not (self.added_files or self.removed_files or self.changed_files)


@dataclass(frozen=True)
class SaveResult(JsonResult):
    """Outcome of saving a model definition."""

    destination: Path
    changed_files: tuple[str, ...] = ()
