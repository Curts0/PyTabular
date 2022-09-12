#


## Tabular
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L26)
```python 
Tabular(
   CONNECTION_STR: str
)
```


---
Tabular Class to perform operations: [Microsoft.AnalysisServices.Tabular](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet)


**Args**

* **CONNECTION_STR** (str) : Valid [Connection String](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions) for connecting to a Tabular Model.



**Methods:**


### .Reload_Model_Info
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L58)
```python
.Reload_Model_Info()
```

---
Runs on __init__ iterates through details, can be called after any model changes. Called in SaveChanges()


**Returns**

* **bool**  : True if successful


### .Disconnect
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L70)
```python
.Disconnect()
```

---
Disconnects from Model


**Returns**

* **bool**  : True if successful


### .Refresh
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L78)
```python
.Refresh(
   Object: Union[str, Table, Partition, Dict[str, Any]],
   RefreshType: RefreshType = RefreshType.Full, Tracing = False
)
```

---
Refreshes table(s) and partition(s).


**Args**

* **Object** (Union[ str, Table, Partition, Dict[str, Any], Iterable[str, Table, Partition, Dict[str, Any]] ]) : Designed to handle a few different ways of selecting a refresh.  
* **RefreshType** (RefreshType, optional) : See [RefreshType](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.refreshtype?view=analysisservices-dotnet). Defaults to RefreshType.Full.
* **Tracing** (bool, optional) : Currently just some basic tracing to track refreshes. Defaults to False.
str == 'Table_Name'  
Table == Table Object  
Partition == Partition Object  
Dict[str, Any] == A way to specify a partition of group of partitions. For ex. {'Table_Name':'Partition1'} or {'Table_Name':['Partition1','Partition2']}. NOTE you can also change out the strings for partition or tables objects.


**Raises**

* **Exception**  : Raises exception if unable to find table or partition via string.



**Returns**

* **WIP**  : WIP


### .Update
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L171)
```python
.Update(
   UpdateOptions: UpdateOptions = UpdateOptions.ExpandFull
)
```

---
[Update Model](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.majorobject.update?view=analysisservices-dotnet#microsoft-analysisservices-majorobject-update(microsoft-analysisservices-updateoptions))


**Args**

* **UpdateOptions** (UpdateOptions, optional) : See above MS Doc link. Defaults to UpdateOptions.ExpandFull.


**Returns**

* **None**  : Placeholder to eventually change.


### .SaveChanges
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L182)
```python
.SaveChanges()
```


### .Backup_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L204)
```python
.Backup_Table(
   table_str: str
)
```

---
USE WITH CAUTION, EXPERIMENTAL. Backs up table in memory, brings with it measures, columns, hierarchies, relationships, roles, etc.  
It will add suffix '_backup' to all objects.  
Refresh is performed from source during backup.


**Args**

* **table_str** (str, optional) : Name of Table.


**Returns**

* **bool**  : Returns True if Successful, else will return error.


### .Revert_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L271)
```python
.Revert_Table(
   table_str: str
)
```

---
USE WITH CAUTION, EXPERIMENTAL. This is used in conjunction with Backup_Table().
It will take the 'TableName_backup' and replace with the original.
Example scenario -> 
1. model.Backup_Table('TableName')
2. perform any proposed changes in original 'TableName'
3. validate changes in 'TableName'
4. if unsuccessful run model.Revert_Table('TableName')


**Args**

* **table_str** (str) : Name of table.


**Returns**

* **bool**  : Returns True if Successful, else will return error.


### .Query
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L336)
```python
.Query(
   Query_Str: str
)
```

---
Executes Query on Model and Returns Results in Pandas DataFrame


**Args**

* **Query_Str** (str) : Dax Query. Note, needs full syntax (ex: EVALUATE). See (DAX Queries)[https://docs.microsoft.com/en-us/dax/dax-queries].  
Will check if query string is a file. If it is, then it will perform a query on whatever is read from the file.  
It is also possible to query DMV. For example. Query("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"). See (DMVs)[https://docs.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions]


**Returns**

* **DataFrame**  : Returns dataframe with results


### .Query_Every_Column
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L377)
```python
.Query_Every_Column(
   query_function: str = 'COUNTROWS(VALUES(_))'
)
```

---
This will dynamically create a query to pull all columns from the model and run the query function.
<br/>It will replace the _ with the column to run.


**Args**

* **query_function** (str, optional) : Dax query is dynamically building a query with the UNION & ROW DAX Functions.


**Returns**

* **DataFrame**  : Returns dataframe with results.


### .Query_Every_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L399)
```python
.Query_Every_Table(
   query_function: str = 'COUNTROWS(_)'
)
```

---
This will dynamically create a query to pull all tables from the model and run the query function.
It will replace the _ with the table to run.


**Args**

* **query_function** (str, optional) : Dax query is dynamically building a query with the UNION & ROW DAX Functions. Defaults to 'COUNTROWS(_)'.


**Returns**

* **DataFrame**  : Returns dataframe with results


### .Analyze_BPA
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L419)
```python
.Analyze_BPA(
   Tabular_Editor_Exe: str, Best_Practice_Analyzer: str
)
```

---
Takes your Tabular Model and performs TE2s BPA. Runs through Command line.
[Tabular Editor BPA](https://docs.tabulareditor.com/te2/Best-Practice-Analyzer.html)
[Tabular Editor Command Line Options](https://docs.tabulareditor.com/te2/Command-line-Options.html)


**Args**

* **Tabular_Editor_Exe** (str) : TE2 Exe File path. Feel free to use class TE2().EXE_Path or provide your own.
* **Best_Practice_Analyzer** (str) : BPA json file path. Feel free to use class BPA().Location or provide your own. Defualts to        https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json


**Returns**

* Assuming no failure, will return list of BPA violations. Else will return error from command line.


### .Create_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L443)
```python
.Create_Table(
   df: pd.DataFrame, table_name: str
)
```

---
Creates tables from pd.DataFrame as an M-Partition. 
So will convert the dataframe to M-Partition logic via the M query table constructor.
Runs refresh and will update model.


**Args**

* **df** (pd.DataFrame) : DataFrame to add to model
* **table_name** (str) : _description_


**Returns**

* **bool**  : True if successful

