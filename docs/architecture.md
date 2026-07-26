# Architecture

## Public facade

`pytabular.Tabular` is the canonical entry point:

- `Tabular(connection_string)` and `Tabular.connect(...)` defer to the legacy
  live XMLA implementation.
- `Tabular.from_tmdl(...)` and `Tabular.from_pbip(...)` return an offline model
  backed by a TMDL definition folder.

Both expose TOM-style uppercase collections. New code can use PEP 8 aliases.

## Runtime boundary

Importing `pytabular` only defines lazy exports and a logger with a null
handler. `_runtime.py` initializes CoreCLR and loads Analysis Services
assemblies only when TOM or ADOMD functionality is requested.

Microsoft assemblies are restored from pinned NuGet packages by
`tools/restore-runtime.ps1`. Release wheels contain those generated runtime
files, so installed users do not manage DLL paths.

## Source boundary

`TmdlSource` owns folder resolution, TOM serialization, validation, snapshots,
and canonical file-oriented diffs. A later milestone can implement a live
source behind the same boundary without coupling offline tests to XMLA.

## Deferred work

Direct Lake-specific helpers, an agent CLI, MCP, Fabric deployment, and broad
wrappers for newer semantic-model objects are not part of 0.6.
