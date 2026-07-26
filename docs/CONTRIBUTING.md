# Contributing

PyTabular aims to make Python a first-class local development language for
tabular semantic models.

## Setup

Use Python 3.11–3.14 and the .NET 8 SDK:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev,all]"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\restore-runtime.ps1
```

The runtime script restores the pinned Microsoft Analysis Services NuGet
packages into `pytabular/_vendor`. Generated assemblies are ignored by Git but
included in release wheels.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Default tests are offline. They must not launch Power BI Desktop, discover a
local instance, connect to Fabric, or mutate a live semantic model.

The preserved legacy Desktop suite is opt-in:

```powershell
$env:PYTABULAR_RUN_LEGACY_DESKTOP_TESTS = "1"
.\.venv\Scripts\python.exe -m pytest test -m desktop
```

Fabric tests require an explicitly supplied test model:

```powershell
$env:PYTABULAR_TEST_CONNECTION_STRING = "<test model connection string>"
.\.venv\Scripts\python.exe -m pytest -m fabric
```

Never point mutating integration tests at a production or client model.

## Pull requests

Run pytest, Ruff, Pyright, the strict documentation build, and a wheel build.
Keep compatibility changes documented in the migration guide.
