from lib2to3.pytree import Base
import logging
import random
import xmltodict
from typing import List, Callable
from Microsoft.AnalysisServices.Tabular import Trace, TraceEvent, TraceEventHandler
from Microsoft.AnalysisServices import TraceColumn, TraceEventClass, TraceEventSubclass



class Base_Trace:
	def __init__(self, Tabular_Class, Trace_Events:List[TraceEvent], Trace_Event_Columns:List[TraceColumn], Handler:Callable) -> None:
		logging.debug(f'Trace Base Class initializing...')
		self.Name = 'PyTabular_'+''.join(random.SystemRandom().choices([str(x) for x in [y for y in range(0,10)]], k=10))
		self.ID = self.Name.replace('PyTabular_', '')
		self.Trace = Trace(self.Name, self.ID)
		logging.debug(f'Trace {self.Trace.Name} created...')
		self.Tabular_Class = Tabular_Class
		self.Event_Categories = self.Query_DMV_For_Event_Categories()

		self.Trace_Events = Trace_Events
		self.Trace_Event_Columns = Trace_Event_Columns
		self.Handler = Handler

		self.Build()
		self.Add()
		self.Update()

	def Build(self):
		logging.info(f'Building Trace {self.Name}')
		TE = [TraceEvent(trace_event) for trace_event in self.Trace_Events]
		logging.debug(f'Adding Events to... {self.Trace.Name}')
		[self.Trace.get_Events().Add(te) for te in TE]

		def add_column(trace_event,trace_event_column):
			try:
				trace_event.Columns.Add(trace_event_column)
			except:
				logging.warning(f'{trace_event} - {trace_event_column} Skipped')
		
		logging.debug(f'Adding Trace Event Columns...')
		[add_column(trace_event,trace_event_column) for trace_event_column in self.Trace_Event_Columns for trace_event in TE if str(trace_event_column.value__) in self.Event_Categories[str(trace_event.EventID.value__)] ]

		logging.debug(f'Adding Handler to Trace...')
		self.Handler = TraceEventHandler(self.Handler)
		self.Trace.OnEvent += self.Handler
		return True
	
	def Arguments(Trace_Events: List[TraceEvent], Trace_Event_Columns: List[TraceColumn], Handler: Callable):
		raise NotImplementedError

	def Add(self):
		logging.info(f'Adding {self.Name} to {self.Tabular_Class.Server.Name}')
		return self.Tabular_Class.Server.Traces.Add(self.Trace)

	def Update(self):
		logging.info(f'Updating {self.Name} in {self.Tabular_Class.Server.Name}')
		return self.Trace.Update()

	def Start(self):
		logging.info(f'Starting {self.Name} in {self.Tabular_Class.Server.Name}')
		return self.Trace.Start()

	def Stop(self):
		logging.info(f'Stopping {self.Name} in {self.Tabular_Class.Server.Name}')
		return self.Trace.Stop()

	def Drop(self):
		logging.info(f'Dropping {self.Name} in {self.Tabular_Class.Server.Name}')
		return self.Trace.Drop()

	def Query_DMV_For_Event_Categories(self):
		Event_Categories = {}
		events = []
		logging.debug(f'Querying DMV for columns rules...')
		logging.debug(f'select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES')
		df = self.Tabular_Class.Query("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES")
		for index, row in df.iterrows():
			xml_data = xmltodict.parse(row.Data)
			if type(xml_data['EVENTCATEGORY']['EVENTLIST']['EVENT']) == list:
				events += [event  for event in xml_data['EVENTCATEGORY']['EVENTLIST']['EVENT'] ]
			else:
				events += [xml_data['EVENTCATEGORY']['EVENTLIST']['EVENT']]
		for event in events:
			Event_Categories[event['ID']] = [column['ID'] for column in event['EVENTCOLUMNLIST']['EVENTCOLUMN']]
		return Event_Categories


def default_refresh_handler(source, args):
	if args.EventSubclass == TraceEventSubclass.ReadData:
		logging.debug(f'{args.ProgressTotal} - {args.ObjectPath}')
	else:
		logging.debug(f'{args.EventClass} - {args.EventSubclass} - {args.ObjectName}')

class Refresh_Trace(Base_Trace):
	def __init__(self, Tabular_Class, Trace_Events: List[TraceEvent] = [TraceEventClass.ProgressReportBegin,TraceEventClass.ProgressReportCurrent,TraceEventClass.ProgressReportEnd,TraceEventClass.ProgressReportError],
	Trace_Event_Columns: List[TraceColumn] = [TraceColumn.EventSubclass,TraceColumn.CurrentTime, TraceColumn.ObjectName, TraceColumn.ObjectPath, TraceColumn.DatabaseName, TraceColumn.SessionID, TraceColumn.TextData, TraceColumn.EventClass, TraceColumn.ProgressTotal],
	Handler: Callable = default_refresh_handler) -> None:
		super().__init__(Tabular_Class, Trace_Events, Trace_Event_Columns, Handler)