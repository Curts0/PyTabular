# TMDL models

Load and validate an offline definition:

```python
from pytabular import Tabular

model = Tabular.from_tmdl("Sales.SemanticModel/definition")
model.validate().raise_for_errors()
```

PBIP projects are resolved to their semantic-model definition:

```python
model = Tabular.from_pbip("Sales.pbip")
```

Save to a different folder or compare two models:

```python
model.save_tmdl("build/Sales.SemanticModel/definition")
other = Tabular.from_tmdl("Other.SemanticModel/definition")
diff = model.diff(other)
print(diff.to_json())
```

The compatibility wrapper remains available:

:::pytabular.tmdl.Tmdl
