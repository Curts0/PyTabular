"""Tests for stable foundational result objects."""

from __future__ import annotations

import pytest

from pytabular.exceptions import ModelValidationError
from pytabular.results import ModelDiff, ValidationMessage, ValidationReport


def test_result_json_is_deterministic() -> None:
    result = ModelDiff(changed_files=("tables/Sales.tmdl",))
    assert result.to_json() == result.to_json()
    assert '"changed_files": [' in result.to_json()
    assert not result.is_empty


def test_validation_report_raises_for_errors() -> None:
    report = ValidationReport(
        valid=False,
        messages=(ValidationMessage("Broken relationship"),),
    )
    with pytest.raises(ModelValidationError, match="Broken relationship"):
        report.raise_for_errors()
