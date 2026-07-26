"""Offline model source and facade tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from pytabular import Tabular
from pytabular.exceptions import ModelSourceError
from pytabular.sources import TmdlSource, resolve_tmdl_path

from .fakes import FakeDatabase, FakeTable


@pytest.fixture
def definition(tmp_path: Path) -> Path:
    path = tmp_path / "Sales.SemanticModel" / "definition"
    path.mkdir(parents=True)
    (path / "model.tmdl").write_text("model Model\n", encoding="utf-8")
    return path


@pytest.fixture
def fake_runtime(monkeypatch: pytest.MonkeyPatch) -> FakeDatabase:
    database = FakeDatabase()

    def deserialize(_: Path) -> FakeDatabase:
        return database

    def serialize(value: FakeDatabase, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        names = ",".join(table.Name for table in value.Model.Tables)
        (destination / "model.tmdl").write_text(
            f"model {value.Model.Name}\ntables {names}\n",
            encoding="utf-8",
        )

    monkeypatch.setattr("pytabular.sources._deserialize_database", deserialize)
    monkeypatch.setattr("pytabular.sources._serialize_database", serialize)
    return database


def test_resolve_pbip_with_one_semantic_model(definition: Path) -> None:
    pbip = definition.parents[1] / "Sales.pbip"
    pbip.write_text("{}", encoding="utf-8")
    assert resolve_tmdl_path(pbip) == definition


def test_resolve_missing_source_fails_fast(tmp_path: Path) -> None:
    with pytest.raises(ModelSourceError, match="Unable to locate"):
        resolve_tmdl_path(tmp_path / "missing")


def test_offline_tabular_has_legacy_and_pep8_aliases(
    definition: Path,
    fake_runtime: FakeDatabase,
) -> None:
    fake_runtime.Model.Tables.Add(FakeTable("Sales"))
    model = Tabular.from_tmdl(definition)
    assert model.Tables is model.tables
    assert model.Measures is model.measures
    assert model.CompatibilityLevel == 1600
    assert model.capabilities.source_kind == "tmdl"
    assert not model.capabilities.live


def test_offline_save_and_diff(
    definition: Path,
    fake_runtime: FakeDatabase,
    tmp_path: Path,
) -> None:
    original = Tabular.from_tmdl(definition)
    second_path = tmp_path / "Second" / "definition"
    original.save_tmdl(second_path)
    other_source = TmdlSource(second_path, FakeDatabase())
    other = type(original)(other_source)
    other.Model.Tables.Add(FakeTable("Added"))

    diff = original.diff(other)
    assert diff.changed_files == ("model.tmdl",)
    assert "Added" in diff.patches["model.tmdl"]


def test_validation_report_is_returned(
    definition: Path,
    fake_runtime: FakeDatabase,
) -> None:
    model = Tabular.from_tmdl(definition)
    assert model.validate().valid
