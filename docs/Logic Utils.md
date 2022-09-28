#


### ticks_to_datetime
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L11)
```python
.ticks_to_datetime(
   ticks: int
)
```

---
Converts a C# System DateTime Tick into a Python DateTime


**Args**

* **ticks** (int) : [C# DateTime Tick](https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0)


**Returns**

* **datetime**  : [datetime.datetime](https://docs.python.org/3/library/datetime.html)


----


### pandas_datatype_to_tabular_datatype
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L23)
```python
.pandas_datatype_to_tabular_datatype(
   df: pd.DataFrame
)
```

---
WiP takes dataframe columns and gets respective tabular column datatype.  ([NumPy Datatypes](https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html) and [Tabular Datatypes](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datatype?view=analysisservices-dotnet))


**Args**

* **df** (pd.DataFrame) : Pandas DataFrame


**Returns**

* **Dict**  : EX {'col1': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9700>, 'col2': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC8840>, 'col3': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9800>}


----


### pd_dataframe_to_m_expression
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L89)
```python
.pd_dataframe_to_m_expression(
   df: pd.DataFrame
)
```

---
This will take a pandas dataframe and convert to an m expression
For example this DF:
   col1  col2
0   1     3
1   2     4

|
|
V

Will convert to this expression string:
let
Source=#table({"col1","col2"},
{
{"1","3"},{"2","4"}
})
in
Source


**Args**

* **df** (pd.DataFrame) : Pandas DataFrame


**Returns**

* **str**  : Currently only returning string values in your tabular model.


----


### remove_folder_and_contents
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L140)
```python
.remove_folder_and_contents(
   folder_location
)
```

---
Internal used in tabular_editor.py and best_practice_analyzer.py.


**Args**

* **folder_location** (str) : Folder path to remove directory and contents.


----


### remove_suffix
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/logic_utils.py\#L153)
```python
.remove_suffix(
   input_string, suffix
)
```

---
Adding for >3.9 compatiblity. (Stackoverflow Answer)[https://stackoverflow.com/questions/66683630/removesuffix-returns-error-str-object-has-no-attribute-removesuffix]


**Args**

* **input_string** (str) : input string to remove suffix from
* **suffix** (str) : suffix to be removed


**Returns**

* **str**  : input_str with suffix removed

