#


### Return_Zero_Row_Tables
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L8)
```python
.Return_Zero_Row_Tables(
   model: pytabular.Tabular
)
```

---
Returns list of table names of those that are returning isna()


**Args**

* **model** (pytabular.Tabular) : Tabular Model


**Returns**

* List of table names where DAX COUNTROWS('Table Name') is nan or 0.


----


### Table_Last_Refresh_Times
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L22)
```python
.Table_Last_Refresh_Times(
   model: pytabular.Tabular, group_partition: bool = True
)
```

---
Returns pd.DataFrame of tables with their latest refresh time. 
Optional 'group_partition' variable, default is True.
If False an extra column will be include to have the last refresh time to the grain of the partition
Example to add to model model.Create_Table(p.Table_Last_Refresh_Times(model),'RefreshTimes')


**Args**

* **model** (pytabular.Tabular) : Tabular Model
* **group_partition** (bool, optional) : Whether or not you want the grain of the dataframe to be by table or by partition. Defaults to True.


**Returns**

* **DataFrame**  : pd dataframe with the RefreshedTime property: https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition.refreshedtime?view=analysisservices-dotnet#microsoft-analysisservices-tabular-partition-refreshedtime
If group_partition == True and the table has multiple partitions, then df.groupby(by["tables"]).max()
