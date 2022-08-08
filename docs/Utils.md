#


### ticks_to_datetime
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L12)
```python
.ticks_to_datetime(
   ticks: int
)
```

---
Converts a C# System DateTime Tick into a Python DateTime


**Args**

* **ticks** (int) : C# DateTime Tick -> [https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0]


**Returns**

* **datetime**  : datetime.datetime value


----


### pandas_datatype_to_tabular_datatype
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L23)
```python
.pandas_datatype_to_tabular_datatype(
   df: pd.DataFrame
)
```

---
WiP takes dataframe columns and gets respective tabular column datatype. ([NumPy Datatypes](https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html) and [Tabular Datatypes](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datatype?view=analysisservices-dotnet))


**Args**

* **df** (pd.DataFrame) : Pandas DataFrame


**Returns**

* **Dict**  : EX {'col1': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9700>, 'col2': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC8840>, 'col3': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9800>}

