# Contributing Guidelines

## Goal
- Make **Python** a first class citizen for interacting with **Tabular models**.

## Some rules
- See [github actions](https://github.com/Curts0/PyTabular/actions) for checks run on pull request.
- We `docstring-coverage` to check for 100% docstring coverage.
- `flake8` also runs, but with a few extra packages. (pep8-naming, flake8-docstrings).
- Updates of any kind are welcome! Even just letting me know of the issues. Or updating docstrings...
- Limit any extra packages, see `pyproject.toml` for dependencies
- Install pre-commit. Pre-commit will run pytest, flake8, and docstr-coverage before push.
```powershell
pip install pre-commit
pre-commit install --hook-type pre-push
```
- **This will take a while...** pytest will open a PBIX file in repository and run tests on it... Eventually these tests will be run on a model that is not local.

## Documentation help
- Docstrings follow the google docstring convention. See [Example](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- The `flake8-docstrings` will check that google docstring format is followed.
- Docstrings get converted to markdown with the `mkgendocs` package.
- Then gets converted to `readthedocs` site with the `mkdocs` package.

## Misc
- Work will be distributed under a MIT license.