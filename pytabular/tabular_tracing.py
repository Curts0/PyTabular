"""`tabular_tracing.py` handles all tracing capabilities in your model.

It also includes some pre built traces to make life easier.
Feel free to build your own.

Example:
    ```python title="Monitor Queries"
    import pytabular as p
    import logging as l
    model = p.Tabular(CONNECTION_STR)
    query_trace = p.QueryMonitor(model)
    query_trace.start() # (1)

    ###

    p.logger.setLevel(l.DEBUG) # (2)

    ###

    query_trace.stop()
    query_trace.drop() # (3)
    ```

    1. You will now start to see query traces on your model get outputed to your console.
    2. If you want to see the FULL query then set logging to DEBUG.
    3. You can drop on your own, or will get dropped on script exit.
"""
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


class BaseTrace:
    """Generates trace to be run on Server.

    This is the base class to customize the type of Trace you are looking for.
    It's recommended to use the out of the box traces built.
    It's on the roadmap to have an intuitive way to build traces for users.
    """

    def __init__(
        self,
        tabular_class,
        trace_events: List[TraceEvent],
        trace_event_columns: List[TraceColumn],
        handler: Callable,
    ) -> None:
        """This will `build()`, `add()`, and `update()` the trace to model.

        It will also register the dropping on the trace on exiting python.

        Args:
            tabular_class (Tabular): The model you want the trace for.
            trace_events (List[TraceEvent]): The TraceEvents you want have in your trace.
                From Microsoft.AnalysisServices.TraceEventClass.
            trace_event_columns (List[TraceColumn]): The trace event columns you want in your trace.
                From Microsoft.AnalysisServices.TraceColumn.
            handler (Callable): The `handler` is a function that will take in two args.
                The first arg is `source` and it is currently unused.
                The second is arg is `args` and here
                is where you can access the results of the trace.
        """
        logger.debug("Trace Base Class initializing...")
        self.Name = "PyTabular_" + "".join(
            random.SystemRandom().choices(
                [str(x) for x in [y for y in range(0, 10)]], k=10
            )
        )
        self.ID = self.Name.replace("PyTabular_", "")
        self.Trace = Trace(self.Name, self.ID)
        logger.debug(f"Trace {self.Trace.Name} created...")
        self.tabular_class = tabular_class
        self.Event_Categories = self._query_dmv_for_event_categories()

        self.trace_events = trace_events
        self.trace_event_columns = trace_event_columns
        self.handler = handler

        self.build()
        self.add()
        self.update()
        atexit.register(self.drop)

    def build(self) -> bool:
        """Run on init.

        This will take the inputed arguments for the class
        and attempt to build the Trace.

        Returns:
                bool: True if successful
        """
        logger.info(f"Building Trace {self.Name}")
        te = [TraceEvent(trace_event) for trace_event in self.trace_events]
        logger.debug(f"Adding Events to... {self.Trace.Name}")
        [self.Trace.get_Events().Add(t) for t in te]

        def add_column(trace_event, trace_event_column):
            """Adds the column to trace event."""
            try:
                trace_event.Columns.Add(trace_event_column)
            except Exception:
                logger.warning(f"{trace_event} - {trace_event_column} Skipped")
                pass

        logger.debug("Adding Trace Event Columns...")
        [
            add_column(trace_event, trace_event_column)
            for trace_event_column in self.trace_event_columns
            for trace_event in te
            if str(trace_event_column.value__)
            in self.Event_Categories[str(trace_event.EventID.value__)]
        ]

        logger.debug("Adding Handler to Trace...")
        self.handler = TraceEventHandler(self.handler)
        self.Trace.OnEvent += self.handler
        return True

    def add(self) -> int:
        """Runs on init. Adds built trace to the Server.

        Returns:
                int: Return int of placement in Server.Traces.get_Item(int).
        """
        logger.info(f"Adding {self.Name} to {self.tabular_class.Server.Name}")
        return self.tabular_class.Server.Traces.Add(self.Trace)

    def update(self) -> None:
        """Runs on init. Syncs with Server.

        Returns:
            None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Updating {self.Name} in {self.tabular_class.Server.Name}")
        if self.tabular_class.Server.Connected is False:
            self.tabular_class.reconnect()

        return self.Trace.Update()

    def start(self) -> None:
        """Call when you want to start the trace.

        Returns:
            None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Starting {self.Name} in {self.tabular_class.Server.Name}")
        return self.Trace.Start()

    def stop(self) -> None:
        """Call when you want to stop the trace.

        Returns:
            None: Returns None.
                Unless unsuccessful then it will return the error from Server.
        """
        logger.info(f"Stopping {self.Name} in {self.tabular_class.Server.Name}")
        return self.Trace.Stop()

    def drop(self) -> None:
        """Call when you want to drop the trace.

        Returns:
            None: Returns None. Unless unsuccessful,
                then it will return the error from Server.
        """
        logger.info(f"Dropping {self.Name} in {self.tabular_class.Server.Name}")
        atexit.unregister(self.drop)
        return self.Trace.Drop()

    def _query_dmv_for_event_categories(self):
        """Internal use. Called during the building process of a refresh.

        It is used to locate allowed columns for event categories.
        This is done by executing a `Tabular().Query()`
        on the `DISCOVER_EVENT_CATEGORIES` table in the DMV.
        Then the function will parse the results,
        as it is xml inside of rows.
        """
        event_categories = {}
        events = []
        logger.debug("Querying DMV for columns rules...")
        logger.debug("select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES")
        df = self.tabular_class.query(
            "select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"
        )
        for index, row in df.iterrows():
            xml_data = xmltodict.parse(row.Data)
            if isinstance(xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"], list):
                events += [
                    event for event in xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"]
                ]
            else:
                events += [xml_data["EVENTCATEGORY"]["EVENTLIST"]["EVENT"]]
        for event in events:
            event_categories[event["ID"]] = [
                column["ID"] for column in event["EVENTCOLUMNLIST"]["EVENTCOLUMN"]
            ]
        return event_categories


def _refresh_handler(source, args):
    """Default handler called when `RefreshTrace()` is used.

    It will log various steps of the refresh process.
    Mostly will output the current # of rows read.
    Will output `logger.warning()` if refresh produces zero rows,
    or if a switching dictionary event occurs.
    The rest of the EventSubclass' will output the raw text.
    For example, TabularSequencePoint, TabularRefresh, Process,
    Vertipaq, CompressSegment, TabularCommit, RelationshipBuildPrepare,
    AnalyzeEncodeData, ReadData. If there is anything else not prebuilt
    out for logging, it will dump the arguments int `logger.debug()`.
    """
    text_data = args.TextData.replace("<ccon>", "").replace("</ccon>", "")

    if (
        args.EventClass == TraceEventClass.ProgressReportCurrent
        and args.EventSubclass == TraceEventSubclass.ReadData
    ):
        table_name = args.ObjectPath.split(".")[-2]
        part_name = args.ObjectPath.split(".")[-1]
        logger.info(
            f"{args.ProgressTotal} row read from '{table_name}' - '{part_name}' "
        )

    elif (
        args.EventClass == TraceEventClass.ProgressReportEnd
        and args.EventSubclass == TraceEventSubclass.ReadData
    ):
        if args.ProgressTotal == 0:
            logger.warning(
                f"{' - '.join(args.ObjectPath.split('.')[-2:])} QUERIED {args.ProgressTotal} ROWS!"
            )
        else:
            table_partition = "::".join(args.ObjectPath.split(".")[-2:])
            logger.info(
                f"Finished Reading {table_partition} for {args.ProgressTotal} Rows!"
            )

    elif args.EventSubclass == TraceEventSubclass.SwitchingDictionary:
        logger.warning(f"{text_data}")

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
        logger.info(f"{text_data}")

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
        logger.info(f"{text_data}")

    else:
        logger.debug(f"{args.EventClass}::{args.EventSubclass}::{text_data}")


class RefreshTrace(BaseTrace):
    """Subclass of `BaseTrace()`. Usefull for monitoring refreshes.

    This is the default trace that is run on refreshes.
    It will output all the various details into `logger()`.
    See `_refresh_handler()` for more details on what gets
    put into `logger()`.
    """

    def __init__(
        self,
        tabular_class,
        trace_events: List[TraceEvent] = [
            TraceEventClass.ProgressReportBegin,
            TraceEventClass.ProgressReportCurrent,
            TraceEventClass.ProgressReportEnd,
            TraceEventClass.ProgressReportError,
        ],
        trace_event_columns: List[TraceColumn] = [
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
        handler: Callable = _refresh_handler,
    ) -> None:
        """Init will extend through `BaseTrace()`. But pass through specific params.

        Args:
            tabular_class (Tabular): This is your `Tabular()` class.
            trace_events (List[TraceEvent], optional): Defaults to [
                TraceEventClass.ProgressReportBegin,
                TraceEventClass.ProgressReportCurrent, TraceEventClass.ProgressReportEnd,
                TraceEventClass.ProgressReportError, ].
            trace_event_columns (List[TraceColumn], optional): Defaults to
                [ TraceColumn.EventSubclass, TraceColumn.CurrentTime,
                TraceColumn.ObjectName, TraceColumn.ObjectPath, TraceColumn.DatabaseName,
                TraceColumn.SessionID, TraceColumn.TextData, TraceColumn.EventClass,
                TraceColumn.ProgressTotal, ].
            handler (Callable, optional): _description_. Defaults to _refresh_handler.
        """
        super().__init__(tabular_class, trace_events, trace_event_columns, handler)


def _query_monitor_handler(source, args):
    """Default function used with the `Query_Monitor()` trace.

    Will return query type, user (effective user), application, start time,
    end time, and total seconds of query in `logger.info()`.
    To see full query set logger to debug `logger.setLevel(logging.DEBUG)`.
    """
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


class QueryMonitor(BaseTrace):
    """Subclass of `BaseTrace()`. Usefull for monitoring queries.

    The default handler for `QueryMonitor()` shows full query in `logger.debug()`.
    So you will need to set your logger to `debug()` if you would like to see them.
    Otherwise, will show basic info on who/what is querying.
    """

    def __init__(
        self,
        tabular_class,
        trace_events: List[TraceEvent] = [TraceEventClass.QueryEnd],
        trace_event_columns: List[TraceColumn] = [
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
        handler: Callable = _query_monitor_handler,
    ) -> None:
        """Init will extend through to BaseTrace, but pass through specific params.

        Args:
            tabular_class (Tabular): This is your `Tabular()` class.
                All that will need to provided to successfully init.
            trace_events (List[TraceEvent], optional): Defaults to [TraceEventClass.QueryEnd].
            trace_event_columns (List[TraceColumn], optional): Defaults to
                [ TraceColumn.EventSubclass, TraceColumn.StartTime, TraceColumn.EndTime,
                TraceColumn.Duration, TraceColumn.Severity, TraceColumn.Error,
                TraceColumn.NTUserName, TraceColumn.DatabaseName, TraceColumn.ApplicationName,
                TraceColumn.TextData, ].
            handler (Callable, optional): Defaults to `_query_monitor_handler()`.
        """
        super().__init__(tabular_class, trace_events, trace_event_columns, handler)
        logger.info("Query text lives in DEBUG, adjust logging to see query text.")
