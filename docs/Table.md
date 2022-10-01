#


## PyTable
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/table.py\#L13)
```python 
PyTable(
   object, model
)
```


---
Wrapper for [Microsoft.AnalysisServices.Tabular.Table](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.table?view=analysisservices-dotnet).
With a few other bells and whistles added to it. You can use the table to access the nested Columns and Partitions. WIP


**Attributes**

* **Model**  : Reference to Tabular class
* **Partitions**  : Reference to Table Partitions
* **Columns**  : Reference to Table Columns



**Methods:**


### .Row_Count
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/table.py\#L36)
```python
.Row_Count()
```

---
Method to return count of rows. Simple Dax Query:
`EVALUATE {COUNTROWS('Table Name')}`


**Returns**

* **int**  : Number of rows using [COUNTROWS](https://learn.microsoft.com/en-us/dax/countrows-function-dax).


### .Refresh
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/table.py\#L45)
```python
.Refresh(
   *args, **kwargs
)
```

---
Same method from Model Refresh, you can pass through any extra parameters. For example:
`Tabular().Tables['Table Name'].Refresh(Tracing = True)`

**Returns**

* **DataFrame**  : Returns pandas dataframe with some refresh details


----


## PyTables
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/table.py\#L54)
```python 
PyTables(
   objects
)
```


---
Iterator to handle tables. Accessible via `Tables` attribute in Tabular class.


**Args**

* **PyTable**  : PyTable class

