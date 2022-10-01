#


## PyPartition
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/partition.py\#L11)
```python 
PyPartition(
   object, table
)
```


---
Wrapper for [Microsoft.AnalysisServices.Partition](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition?view=analysisservices-dotnet).
With a few other bells and whistles added to it. WIP


**Args**

* **Table**  : Parent Table to the Column



**Methods:**


### .Last_Refresh
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/partition.py\#L23)
```python
.Last_Refresh()
```

---
Queries `RefreshedTime` attribute in the partition and converts from C# Ticks to Python datetime


**Returns**

* **datetime**  : Last Refreshed time of Partition in datetime format


### .Refresh
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/partition.py\#L31)
```python
.Refresh(
   *args, **kwargs
)
```

---
Same method from Model Refresh, you can pass through any extra parameters. For example:
`Tabular().Tables['Table Name'].Partitions[0].Refresh(Tracing = True)`

**Returns**

* **DataFrame**  : Returns pandas dataframe with some refresh details


----


## PyPartitions
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/partition.py\#L40)
```python 
PyPartitions(
   objects
)
```


