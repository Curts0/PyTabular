# Contributing Guidelines

- Work will be distributed under MIT license.
- See github actions for checks run on pull request.
- Updates of any kind are welcome! Even just letting me know of the issues. Or updating doc strings...
- Limit any external modules, see pyproject.toml for dependencies
- Goal of project is to help connect the python world and the tabular model world for some easier programmatic execution on models. 
- Install pre-commit. Pre-commit will run pytest, flake8, and docstr-coverage before push.
```powershell
pip install pre-commit
pre-commit install --hook-type pre-push
```
- This will take a while... pytest will open a PBIX file in repository and run tests on it.