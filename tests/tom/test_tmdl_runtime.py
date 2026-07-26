"""Offline contract tests against Microsoft's real TOM serializer."""

from __future__ import annotations

from pathlib import Path

from pytabular import Tabular

FIXTURE = Path(__file__).parents[1] / "fixtures" / "minimal" / "definition"


def test_real_tmdl_round_trip(tmp_path: Path) -> None:
    model = Tabular.from_tmdl(FIXTURE)
    assert model.Database.Name == "Sales"
    assert model.Model.Name == "Model"
    assert model.Tables["Sales"].Measures["Total Sales"].Expression == "1"

    destination = tmp_path / "Sales.SemanticModel" / "definition"
    result = model.save_tmdl(destination)
    reloaded = Tabular.from_tmdl(destination)

    assert result.destination == destination
    assert model.diff(reloaded).is_empty
    assert reloaded.validate().valid
