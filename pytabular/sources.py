"""Semantic-model sources backed by TMDL folders."""

from __future__ import annotations

import difflib
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytabular._runtime import load_tom
from pytabular.exceptions import ModelSourceError
from pytabular.results import ModelDiff, SaveResult, ValidationMessage, ValidationReport


def resolve_tmdl_path(path: str | Path) -> Path:
    """Resolve a TMDL definition folder from TMDL, PBIP, or semantic-model paths."""
    candidate = Path(path).expanduser().resolve()
    if candidate.is_file() and candidate.suffix.lower() == ".pbip":
        models = sorted(candidate.parent.glob("*.SemanticModel/definition"))
        if len(models) != 1:
            raise ModelSourceError(
                f"Expected one semantic model beside {candidate.name}; found {len(models)}."
            )
        return models[0]

    if candidate.is_dir() and candidate.name.lower() == "definition":
        return candidate
    if candidate.is_dir() and candidate.name.lower().endswith(".semanticmodel"):
        definition = candidate / "definition"
        if definition.is_dir():
            return definition
    if candidate.is_dir() and (candidate / "model.tmdl").is_file():
        return candidate

    raise ModelSourceError(f"Unable to locate a TMDL definition at {candidate}.")


def _serialize_database(database: Any, destination: Path) -> None:
    serializer = load_tom().TmdlSerializer
    if hasattr(serializer, "SerializeDatabaseToFolder"):
        serializer.SerializeDatabaseToFolder(database, str(destination))
        return
    serializer.SerializeModelToFolder(database.Model, str(destination))


def _deserialize_database(source: Path) -> Any:
    tom = load_tom()
    serializer = tom.TmdlSerializer
    if hasattr(serializer, "DeserializeDatabaseFromFolder"):
        return serializer.DeserializeDatabaseFromFolder(str(source))

    model = serializer.DeserializeModelFromFolder(str(source))
    database = tom.Database()
    database.Name = source.parent.stem or "SemanticModel"
    database.Model = model
    return database


def _definition_files(path: Path) -> dict[str, str]:
    return {
        file.relative_to(path).as_posix(): file.read_text(encoding="utf-8")
        for file in sorted(path.rglob("*.tmdl"))
    }


@dataclass
class TmdlSource:
    """A semantic model stored as a TMDL folder."""

    path: Path
    database: Any

    @classmethod
    def open(cls, path: str | Path) -> TmdlSource:
        """Load a TMDL folder."""
        resolved = resolve_tmdl_path(path)
        try:
            database = _deserialize_database(resolved)
        except Exception as error:
            raise ModelSourceError(
                f"Unable to load TMDL from {resolved}: {error}"
            ) from error
        return cls(resolved, database)

    @property
    def model(self) -> Any:
        """Return the TOM model."""
        return self.database.Model

    def save(self, path: str | Path | None = None) -> SaveResult:
        """Serialize the database to its source or a new folder."""
        destination = Path(path).expanduser().resolve() if path else self.path
        destination.mkdir(parents=True, exist_ok=True)
        before = _definition_files(destination)
        _serialize_database(self.database, destination)
        after = _definition_files(destination)
        changed = tuple(
            sorted(
                name
                for name in set(before) | set(after)
                if before.get(name) != after.get(name)
            )
        )
        if path:
            self.path = destination
        return SaveResult(destination=destination, changed_files=changed)

    def snapshot(self) -> dict[str, str]:
        """Return canonical serialized TMDL files without changing the source."""
        with tempfile.TemporaryDirectory(prefix="pytabular-") as temp:
            destination = Path(temp)
            _serialize_database(self.database, destination)
            return _definition_files(destination)

    def validate(self) -> ValidationReport:
        """Validate the TOM model and normalize validation messages."""
        validator = getattr(self.model, "Validate", None)
        if validator is None:
            return ValidationReport(valid=True)
        try:
            raw = validator()
        except Exception as error:
            return ValidationReport(
                valid=False,
                messages=(ValidationMessage(message=str(error)),),
            )

        messages: list[ValidationMessage] = []
        errors = getattr(raw, "Errors", raw)
        if errors is not None:
            try:
                iterator = errors.GetEnumerator()
            except AttributeError:
                iterator = iter(errors)
            for item in iterator:
                severity = str(getattr(item, "Severity", "error")).lower()
                messages.append(
                    ValidationMessage(
                        message=str(getattr(item, "Message", item)),
                        severity=severity,
                        code=str(getattr(item, "Code", "")) or None,
                        path=str(getattr(item, "ObjectPath", "")) or None,
                    )
                )
        contains_errors = bool(getattr(raw, "ContainsErrors", False))
        valid = not contains_errors and not any(
            message.severity == "error" for message in messages
        )
        return ValidationReport(valid=valid, messages=tuple(messages))


def diff_sources(left: TmdlSource, right: TmdlSource) -> ModelDiff:
    """Return a canonical, file-oriented TMDL diff."""
    before = left.snapshot()
    after = right.snapshot()
    before_names = set(before)
    after_names = set(after)
    changed = sorted(
        name for name in before_names & after_names if before[name] != after[name]
    )
    patches = {
        name: "".join(
            difflib.unified_diff(
                before[name].splitlines(keepends=True),
                after[name].splitlines(keepends=True),
                fromfile=f"a/{name}",
                tofile=f"b/{name}",
            )
        )
        for name in changed
    }
    return ModelDiff(
        added_files=tuple(sorted(after_names - before_names)),
        removed_files=tuple(sorted(before_names - after_names)),
        changed_files=tuple(changed),
        patches=patches,
    )
