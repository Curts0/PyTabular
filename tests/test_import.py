"""Import behavior must stay free of runtime side effects."""

from __future__ import annotations

import subprocess
import sys


def test_import_is_quiet_and_does_not_load_clr() -> None:
    command = (
        "import sys; import pytabular; "
        "assert 'clr' not in sys.modules; "
        "assert 'Microsoft.AnalysisServices.Tabular' not in sys.modules"
    )
    result = subprocess.run(
        [sys.executable, "-c", command],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    assert result.stderr == ""


def test_public_tabular_is_lazy() -> None:
    import pytabular

    assert "pytabular._legacy" not in sys.modules
    assert pytabular.Tabular.__name__ == "Tabular"
    assert "pytabular._legacy" not in sys.modules
