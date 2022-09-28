#


## Base_Trace
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L11)
```python 
Base_Trace(
   Tabular_Class, Trace_Events: List[TraceEvent],
   Trace_Event_Columns: List[TraceColumn], Handler: Callable
)
```


---
Generates Trace to be run on Server.
This is the base class to customize the type of Trace you are looking for.
[Server Traces](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.server.traces?view=analysisservices-dotnet#microsoft-analysisservices-tabular-server-traces)


**Args**

* **Tabular_Class** (Tabular) : Tabular Class.
* **Trace_Events** (List[TraceEvent]) : List of Trace Events.
* **Trace_Event_Columns** (List[TraceColumn]) : List of Trace Event Columns.
* **Handler** (Callable) : Function to call when Trace returns response.
[TraceEventClass](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventclass?view=analysisservices-dotnet)
[TraceEventColumn](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tracecolumn?view=analysisservices-dotnet)
Input needs to be two arguments.
One is source (Which is currently None... Need to investigate why).
Second is
[TraceEventArgs](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventargs?view=analysisservices-dotnet)


**Methods:**


### .Build
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L56)
```python
.Build()
```

---
Run on initialization.
This will take the inputed arguments for the class
and attempt to build the Trace.


**Returns**

* **bool**  : True if successful


### .Arguments
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L90)
```python
.Arguments(
   Trace_Events: List[TraceEvent], Trace_Event_Columns: List[TraceColumn],
   Handler: Callable
)
```


### .Add
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L97)
```python
.Add()
```

---
Runs on initialization. Adds built Trace to the Server.


**Returns**

* **int**  : Return int of placement in Server.Traces.get_Item(int)


### .Update
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L106)
```python
.Update()
```

---
Runs on initialization. Syncs with Server.


**Returns**

* **None**  : Returns None.
Unless unsuccessful then it will return the error from Server.

### .Start
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L116)
```python
.Start()
```

---
Call when you want to start the Trace


**Returns**

* **None**  : Returns None.
Unless unsuccessful then it will return the error from Server.

### .Stop
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L126)
```python
.Stop()
```

---
Call when you want to stop the Trace


**Returns**

* **None**  : Returns None.
Unless unsuccessful then it will return the error from Server.

### .Drop
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L136)
```python
.Drop()
```

---
Call when you want to drop the Trace


**Returns**

* **None**  : Returns None. Unless unsuccessful,
then it will return the error from Server.

----


## Refresh_Trace
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_tracing.py\#L187)
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
   Handler: Callable = refresh_handler
)
```


---
Subclass of Base_Trace. For built-in Refresh Tracing.


**Args**

* **Base_Trace** (_type_) : _description_

