#


## Tabular
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L32)
```python 
Tabular(
   CONNECTION_STR: str
)
```


---
Tabular Class to perform operations:[Microsoft.AnalysisServices.Tabular](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet)


**Args**

* **CONNECTION_STR** (str) : [Connection String](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions)



**Methods:**


### .Disconnect
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L65)
```python
.Disconnect()
```

---
Disconnects from Model


**Returns**

* **bool**  : True if successful


### .Refresh
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L80)
```python
.Refresh(
   iterable_items: List, RefreshType = RefreshType.Full
)
```

---
Input iterable Collections for the function to run through.
It will add the collection items into a Refresh Request.
To execute refresh run through Update()


**Args**

* **iterable_items** (List) : Must be refreshable Tabular objects.
* **RefreshType** (_type_, optional) : _description_. Defaults to RefreshType.Full.


### .Update
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L92)
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


### .Backup_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L103)
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
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L170)
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
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L238)
```python
.Query(
   Query_Str: str
)
```

---
Executes Query on Model and Returns Results in Pandas DataFrame


**Args**

* **Query_Str** (str) : Dax Query. Note, needs full syntax (ex: EVALUATE). See https://docs.microsoft.com/en-us/dax/dax-queries 


**Returns**

* **DataFrame**  : Returns dataframe with results


### .Query_Every_Column
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L268)
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
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L290)
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
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L310)
```python
.Analyze_BPA(
   Tabular_Editor_Exe: str, Best_Practice_Analyzer: str
)
```

---
Takes your Tabular Model and performs TE2s BPA. Runs through Command line.
https://docs.tabulareditor.com/te2/Best-Practice-Analyzer.html
https://docs.tabulareditor.com/te2/Command-line-Options.html


**Args**

* **Tabular_Editor_Exe** (str) : TE2 Exe File path. Feel free to use class TE2().EXE_Path or provide your own.
* **Best_Practice_Analyzer** (str) : BPA json file path. Feel free to use class BPA().Location or provide your own. Defualts to        https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json


**Returns**

* Assuming no failure, will return list of BPA violations. Else will return error from command line.


### .Create_Table
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/pytabular.py\#L334)
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

