#


## Base_Trace
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L10)
```python 
Base_Trace(
   Tabular_Class, Trace_Events: List[TraceEvent],
   Trace_Event_Columns: List[TraceColumn], Handler: Callable
)
```




**Methods:**


### .Build
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L37)
```python
.Build()
```

---
Run on initialization. This will take the inputed arguments for the class and attempt to build the Trace.


**Returns**

* **bool**  : True if successful


### .Arguments
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L62)
```python
.Arguments(
   Trace_Events: List[TraceEvent], Trace_Event_Columns: List[TraceColumn],
   Handler: Callable
)
```


### .Add
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L65)
```python
.Add()
```

---
Runs on initialization. Adds built Trace to the Server.


**Returns**

* **int**  : Return int of placement in Server.Traces.get_Item(int)


### .Update
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L74)
```python
.Update()
```

---
Runs on initialization. Syncs with Server. 


**Returns**

* **None**  : Returns None. Unless unsuccessful then it will return the error from Server.


### .Start
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L83)
```python
.Start()
```

---
Call when you want to start the Trace


**Returns**

* **None**  : Returns None. Unless unsuccessful then it will return the error from Server.


### .Stop
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L92)
```python
.Stop()
```

---
Call when you want to stop the Trace


**Returns**

* **None**  : Returns None. Unless unsuccessful then it will return the error from Server.


### .Drop
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L101)
```python
.Drop()
```

---
Call when you want to drop the Trace


**Returns**

* **None**  : Returns None. Unless unsuccessful then it will return the error from Server.


### .Query_DMV_For_Event_Categories
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L110)
```python
.Query_DMV_For_Event_Categories()
```

---
Internal use. Called during the building process to locate allowed columns for event categories. This is done by executing a Tabular().Query() on the DISCOVER_EVENT_CATEGORIES table in the DMV. Then the function will parse the results, as it is xml inside of rows.


**Returns**

* **_type_**  : _description_


----


## Refresh_Trace
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L138)
```python 
Refresh_Trace(
   Tabular_Class,
   Trace_Events: List[TraceEvent] = [TraceEventClass.ProgressReportBegin,
   TraceEventClass.ProgressReportCurrent, TraceEventClass.ProgressReportEnd,
   TraceEventClass.ProgressReportError],
   Trace_Event_Columns: List[TraceColumn] = [TraceColumn.EventSubclass,
   TraceColumn.CurrentTime, TraceColumn.ObjectName, TraceColumn.ObjectPath,
   TraceColumn.DatabaseName, TraceColumn.SessionID, TraceColumn.TextData,
   TraceColumn.EventClass, TraceColumn.ProgressTotal],
   Handler: Callable = default_refresh_handler
)
```


---
Subclass of Base_Trace. For built-in Refresh Tracing.


**Args**

* **Base_Trace** (_type_) : _description_

