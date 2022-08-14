import logging
import pytabular
import localsecret as l
from Microsoft.AnalysisServices.Tabular import Trace, TraceEvent, TraceEventHandler
from Microsoft.AnalysisServices import TraceEventClass, TraceEventCollection, TraceColumn, UpdateOptions
a = Trace('TestingTraces','abc')
#a.LogFileName = 'TestingTracing.trc'
#a.LogFileSize = 10
#a.LogFileRollover = True
#a.LogFileAppend = True

def handler(source, args):
    print('my_handler called!')
b = TraceEventHandler(handler)
a.Description = 'Tracing Example'
trace_event_list = [TraceEventClass.ProgressReportBegin,TraceEventClass.ProgressReportCurrent,TraceEventClass.ProgressReportEnd,TraceEventClass.ProgressReportError]

for trace_event in trace_event_list:
	te = TraceEvent(trace_event)
	[te.Columns.Add(t) for t in [TraceColumn.EventSubclass,TraceColumn.CurrentTime, TraceColumn.ObjectName, TraceColumn.ObjectPath, TraceColumn.DatabaseName, TraceColumn.SessionID, TraceColumn.TextData]]
	a.get_Events().Add(te)
a.OnEvent += b #THIS IS HOW YOU DO IT!!!!!! HOT FREAKING DAMN
#Columns 1,2,13,14,28,39,42
#EventSubclass, CurrentTime, ObjectName, ObjectPath, DatabaseName, SessionID, TextData
#model = pytabular.Tabular(l.CONNECTION_STR['FIN 500'])
#model.Server.Traces.Add(a)
#a.Update() #To officially add trace to model
#https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.traceevent?view=analysisservices-dotnet
#https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventclass?view=analysisservices-dotnet
#https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventhandler?view=analysisservices-dotnet
#https://docs.microsoft.com/en-us/sql/relational-databases/sql-trace/sql-trace?view=sql-server-ver16
#! It's get_Events() not Events to add the darn TraceEvents
#! Need to SaveChange() instead of update...
#Trace().Drop() to actually get rid of it...
#select * from $SYSTEM.DISCOVER_JOBS

