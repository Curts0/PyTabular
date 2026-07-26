# Working on PyTabular

PyTabular is a local-first semantic-model library. Keep the default development
loop offline and deterministic.

## Rules

- Do not launch Power BI Desktop, discover local instances, or connect to
  Fabric from default tests.
- Put Desktop tests behind the `desktop` marker and Fabric tests behind the
  `fabric` marker.
- Do not commit generated files from `pytabular/_vendor`, `runtime/bin`, or
  `runtime/obj`.
- Keep `import pytabular` free of CLR, logging, process, filesystem, and network
  side effects.
- Preserve `Tabular(connection_string)` and existing uppercase collection
  attributes while the 0.x compatibility period is active.
- Prefer small typed adapters around TOM rather than duplicating TOM objects in
  Python.

## Checks

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\restore-runtime.ps1
python -m pytest
ruff check pytabular tests
ruff format --check pytabular tests
pyright
mkdocs build --strict
python -m build
```
