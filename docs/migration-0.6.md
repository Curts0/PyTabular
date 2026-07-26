# Migrating to 0.6

Version 0.6 preserves the main live API:

```python
from pytabular import Tabular

model = Tabular(CONNECTION_STRING)
model.Tables["Sales"].refresh()
```

PEP 8 collection aliases are also available:

```python
model.tables["Sales"].refresh()
```

## Dependency extras

Pandas-based queries and Desktop-oriented utilities are no longer required by
the offline model core:

```powershell
python -m pip install "python-tabular[query]"
python -m pip install "python-tabular[desktop]"
```

Use `python-tabular[all]` for the closest match to the 0.5 installation.

## Imports

`import pytabular` no longer configures application logging or loads CLR.
Applications should configure Python logging themselves.

## TMDL

Use `Tabular.from_tmdl(path)` for a definition folder or
`Tabular.from_pbip(path)` for a PBIP project. `save_tmdl`, `validate`, and
`diff` operate without connecting to a model server.
