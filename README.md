# PyTabular

PyTabular provides local-first Python tooling for Power BI and Analysis Services
tabular semantic models.

Version 0.6 modernizes the original package around two explicit workflows:

- connect to a live XMLA model with `Tabular(connection_string)`;
- load an offline TMDL or PBIP model with `Tabular.from_tmdl(path)` or
  `Tabular.from_pbip(path)`.

```python
from pytabular import Tabular

model = Tabular.from_tmdl("Sales.SemanticModel/definition")
report = model.validate()
report.raise_for_errors()
model.save_tmdl("build/Sales.SemanticModel/definition")
```

Live querying and Power BI Desktop helpers are optional:

```powershell
python -m pip install "python-tabular[query]"
python -m pip install "python-tabular[desktop]"
```

## Development

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev,all]"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\restore-runtime.ps1
.\.venv\Scripts\python.exe -m pytest
```

Default tests are offline. They do not launch Power BI Desktop or connect to
Fabric. See [the contribution guide](docs/CONTRIBUTING.md) for opt-in
integration testing.
