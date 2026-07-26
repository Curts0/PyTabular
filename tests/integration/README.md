# Integration tests

The default test suite is offline.

The original live suite remains under `test/` and is ignored unless
`PYTABULAR_RUN_LEGACY_DESKTOP_TESTS=1` is set. When enabled, every collected
test receives the `desktop` marker and uses the preserved AdventureWorks
fixtures.

Fabric integration tests added in later milestones must use the `fabric`
marker and explicit environment variables. They must never run on ordinary
pull requests.
