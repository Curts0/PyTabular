import logging
import random
import xmltodict
from typing import List, Callable
from Microsoft.AnalysisServices.Tabular import Trace, TraceEvent, TraceEventHandler
from Microsoft.AnalysisServices import (
    TraceColumn,
    TraceEventClass,
    TraceEventSubclass,
)
import atexit

logger = logging.getLogger("PyTabular")


class Base_Trace:
    """Generates Trace to be run on Server.
    This is the base class to customize the type of Trace you are looking for.
    [Server Traces](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.server.traces?view=analysisservices-dotnet#microsoft-analysisservices-tabular-server-traces)

    Args:
            Tabular_Class (Tabular): Tabular Class.
            Trace_Events (List[TraceEvent]): List of Trace Events.
            [TraceEventClass](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventclass?view=analysisservices-dotnet)
            Trace_Event_Columns (List[TraceColumn]): List of Trace Event Columns.
            [TraceEventColumn](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tracecolumn?view=analysisservices-dotnet)
            Handler (Callable): Function to call when Trace returns response.
            Input needs to be two arguments.
            One is source (Which is currently None... Need to investigate why).
            Second is
            [TraceEventArgs](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.traceeventargs?view=analysisservices-dotnet)
    """

    def __init__(
        self,
        Tabular_Class,
        Trace_Events: List[TraceEvent],
        Trace_Event_Columns: List[TraceColumn],
        Handler: Callable,
    ) -> None:
        logger.debug("Trace Base Class initializing...")
        self.Name = "PyTabular_" + "".join(
            random.SystemRandom().choices(
                [str(x) for x in [y for y in range(0, 10)]], k=10
            )
        )
        self.ID = self.Name.replace("PyTabular_", "")
        self.Trace = Trace(self.Name, self.ID)
        logger.debug(f"Trace {self.Trace.Name} created...")
        self.Tabular_Class = Tabular_Class
        self.Event_Categories = self._Query_DMV_For_Event_Categories()

        self.Trace_Events = Trace_Events
        self.Trace_Event_Columns = Trace_Event_Columns
        self.Handler = Handler

        self.Build()
        self.Add()
        self.Update()
        atexit.register(self.Drop)

    def Build(self) -> bool:
        """Run on initialization.
        This will take the inputed arguments for the class
        and attempt to build the Trace.

        Returns:
                bool: True if successful
        """
        logger.info(f"Building Trace {self.Name}")
        TE = [TraceEvent(trace_event) for trace_event in self.Trace_Events]
        logger.debug(f"Adding Events to... {self.Trace.Name}")
        [self.Trace.get_Events().Add(te) for te in TE]

        def add_column(trace_event, trace_event_column):
            try:
                trace_event.Columns.Add(trace_event_column)
            except Exception:
                logger.warning(f"{trace_event} - {trace_event_column} Skipped")
                pass

        logger.debug("Adding Trace Event Columns...")
        [
            add_column(trace_event, trace_event_column)
            for trace_event_column in self.Trace_Event_Columns
            for trace_event in TE
            if str(trace_event_column.value__)
            in self.Event_Categories[str(trace_event.EventID.value__)]
        ]

        logger.debug("Adding Handler to Trace...")
        self.Handler = TraceEventHandler(self.Handler)
        self.Trace.OnEvent += self.Handler
        return True

    def Arguments(
        Trace_Events: List[TraceEvent],
        Trace_Event_Columns: List[TraceColumn],
        Handler: Callable,
    ):
        raise NotImplementedError

    def Add(self) -> int:
        """Runs on initialization. Adds built Trace to the Server.

        Returns:
                int: Return int of placement in Server.Traces.get_Item(int)
        """
        logger.info(f"Adding {self.Name} to {self.Tabular_Class.Server.Name}")
        return self.Tabular_Class.Server.Traces.Add(self.Trace)

    def Update(self) -> None:
        """Runs on initialization. Syncs with Server.

        Returns:
                None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Updating {self.Name} in {self.Tabular_Class.Server.Name}")
        return self.Trace.Update()

    def Start(self) -> None:
        """Call when you want to start the Trace

        Returns:
                None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Starting {self.Name} in {self.Tabular_Class.Server.Name}")
        return self.Trace.Start()

    def Stop(self) -> None:
        """Call when you want to stop the Trace

        Returns:
                None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Stopping {self.Name} in {self.Tabular_Class.Server.Name}")
        return self.Trace.Stop()

    def Drop(self) -> None:
        """Call when you want to drop the Trace

        Returns:
                None: Returns None. Unless unsuccessful,
                then it will return the error from Server.
        """
        logger.info(f"Dropping {self.Name} in {self.Tabular_Class.Server.Name}")
        return self.Trace.Drop()

    def _Query_DMV_For_Event_Categories(self):
        """Internal use.
        Called during the building process
        to locate allowed columns for event categories.
        This is done by executing a Tabular().Query()
        on the DISCOVER_EVENT_CATEGORIES table in the DMV.
        Then the function will parse the results,
        as it is xml inside of rows.

        Returns:
                _type_: _description_
        """
        Event_Categories = {}
        events = []
        logger.debug("Querying DMV for columns rules...")
        logger.debug("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES")
        df = self.Tabular_Class.Query(
            "select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"
        )
        for index, row in df.iterrows():
            xml_data = xmltodict.parse(row.Data)
            if type(xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"]) == list:
                events += [
                    event for event in xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"]
                ]
            else:
                events += [xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"]]
        for event in events:
            Event_Categories[event["ID"]] = [
                column["ID"] for column in event["EVENTCOLUMNLIST"]["EVENTCOLUMN"]
            ]
        return Event_Categories


def _refresh_handler(source, args):
    TextData = args.TextData.replace("<ccon>", "").replace("</ccon>", "")

    if (
        args.EventClass == TraceEventClass.ProgressReportCurrent
        and args.EventSubclass == TraceEventSubclass.ReadData
    ):
        logger.info(
            f"Total Rows Read {args.ProgressTotal} From Table '{args.ObjectPath.split('.')[-2]}' Partition '{args.ObjectPath.split('.')[-1]}' "
        )

    elif (
        args.EventClass == TraceEventClass.ProgressReportEnd
        and args.EventSubclass == TraceEventSubclass.ReadData
    ):
        if args.ProgressTotal == 0:
            logger.warning(
                f"{'::'.join(args.ObjectPath.split('.')[-2:])} QUERIED {args.ProgressTotal} ROWS!"
            )
        else:
            logger.info(
                f"Finished Reading {'::'.join(args.ObjectPath.split('.')[-2:])} for {args.ProgressTotal} Rows!"
            )

    elif args.EventSubclass == TraceEventSubclass.SwitchingDictionary:
        logger.warning(f"{TextData}")

    elif (
        args.EventClass == TraceEventClass.ProgressReportBegin
        and args.EventSubclass
        in [
            TraceEventSubclass.TabularSequencePoint,
            TraceEventSubclass.TabularRefresh,
            TraceEventSubclass.Process,
            TraceEventSubclass.VertiPaq,
            TraceEventSubclass.CompressSegment,
            TraceEventSubclass.TabularCommit,
            TraceEventSubclass.RelationshipBuildPrepare,
            TraceEventSubclass.AnalyzeEncodeData,
            TraceEventSubclass.ReadData,
        ]
    ):
        logger.info(f"{TextData}")

    elif (
        args.EventClass == TraceEventClass.ProgressReportEnd
        and args.EventSubclass
        in [
            TraceEventSubclass.TabularSequencePoint,
            TraceEventSubclass.TabularRefresh,
            TraceEventSubclass.Process,
            TraceEventSubclass.VertiPaq,
            TraceEventSubclass.CompressSegment,
            TraceEventSubclass.TabularCommit,
            TraceEventSubclass.RelationshipBuildPrepare,
            TraceEventSubclass.AnalyzeEncodeData,
        ]
    ):
        logger.info(f"{TextData}")

    else:
        logger.debug(f"{args.EventClass}::{args.EventSubclass}::{TextData}")


class Refresh_Trace(Base_Trace):
    """Subclass of Base_Trace. For built-in Refresh Tracing.

    Args:
            Base_Trace (_type_): _description_
    """

    def __init__(
        self,
        Tabular_Class,
        Trace_Events: List[TraceEvent] = [
            TraceEventClass.ProgressReportBegin,
            TraceEventClass.ProgressReportCurrent,
            TraceEventClass.ProgressReportEnd,
            TraceEventClass.ProgressReportError,
        ],
        Trace_Event_Columns: List[TraceColumn] = [
            TraceColumn.EventSubclass,
            TraceColumn.CurrentTime,
            TraceColumn.ObjectName,
            TraceColumn.ObjectPath,
            TraceColumn.DatabaseName,
            TraceColumn.SessionID,
            TraceColumn.TextData,
            TraceColumn.EventClass,
            TraceColumn.ProgressTotal,
        ],
        Handler: Callable = _refresh_handler,
    ) -> None:
        super().__init__(Tabular_Class, Trace_Events, Trace_Event_Columns, Handler)


def _query_monitor_handler(source, args):
    total_secs = args.Duration / 1000
    domain_site = args.NTUserName.find("\\")
    if domain_site > 0:
        user = args.NTUserName[domain_site + 1 :]
    else:
        user = args.NTUserName
    logger.info(f"{args.EventSubclass} by {user} in {args.ApplicationName}")
    logger.info(
        f"From {args.StartTime} to {args.EndTime} for {str(total_secs)} seconds"
    )
    if args.Severity == 3:
        logger.error(f"Query failure... {str(args.Error)}")
        logger.error(f"{args.TextData}")
    logger.debug(f"{args.TextData}")


class Query_Monitor(Base_Trace):
    def __init__(
        self,
        Tabular_Class,
        Trace_Events: List[TraceEvent] = [TraceEventClass.QueryEnd],
        Trace_Event_Columns: List[TraceColumn] = [
            TraceColumn.EventSubclass,
            TraceColumn.StartTime,
            TraceColumn.EndTime,
            TraceColumn.Duration,
            TraceColumn.Severity,
            TraceColumn.Error,
            TraceColumn.NTUserName,
            TraceColumn.DatabaseName,
            TraceColumn.ApplicationName,
            TraceColumn.TextData,
        ],
        Handler: Callable = _query_monitor_handler,
    ) -> None:
        super().__init__(Tabular_Class, Trace_Events, Trace_Event_Columns, Handler)
        logger.info("Query text lives in DEBUG, adjust logging to see query text.")
