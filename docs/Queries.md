#


## Connection
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/query.py\#L11)
```python 
Connection(
   Server
)
```


---
Subclass for [Adomdclient](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.adomdclient?view=analysisservices-dotnet). With some extra items on top.
Right now designed for internal use. For example, Query method in the Tabular class is just a wrapper for this class' Query method... So use that instead.


**Args**

* **AdomdConnection** (_type_) : _description_



**Methods:**


### .Query
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/query.py\#L25)
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

