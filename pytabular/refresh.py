"""
`refresh.py` is the main file to handle all the components of refreshing your model.
"""
from tabular_tracing import RefreshTrace, BaseTrace
import logging
from Microsoft.AnalysisServices.Tabular import (
    RefreshType,
    Table,
    Partition,
)
import pandas as pd
from logic_utils import ticks_to_datetime
from typing import Union, Dict, Any
from table import PyTable, PyTables
from partition import PyPartition
from abc import ABC

logger = logging.getLogger("PyTabular")


class RefreshCheck(ABC):
    """`RefreshCheck` is an assertion you run after your refreshes.
    It will run the given `function` before and after refreshes,
    then run the assertion of before and after. The default given in a refresh is to check row count.
    It will check row count before, and row count after. Then fail if row count after is zero.

    Args:
        name (str): Name of RefreshCheck
        function (function): Function to run before and after refresh.
        assertion (function): Functino that takes a `pre` and `post` argument to output True or False.
    """

    def __init__(self, name: str, function, assertion=None) -> None:
        super().__init__()
        self._name = name
        self._function = function
        self._assertion = assertion
        self._pre = None
        self._post = None

    def __repr__(self) -> str:
        """
        `__repre__` that returns details on `RefreshCheck`.
        """
        return f"{self.name} - {self.pre} - {self.post} - {str(self.function)}"

    @property
    def name(self):
        "Get your custom name of refresh check."
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def function(self):
        "Get the function that is used to run a pre and post check."
        return self._function

    @function.setter
    def function(self, func):
        self._function = func

    @function.deleter
    def function(self):
        del self._function

    @property
    def pre(self):
        "Get the pre value that is the result from the pre refresh check."
        return self._pre

    @pre.setter
    def pre(self, pre):
        self._pre = pre

    @pre.deleter
    def pre(self):
        del self._pre

    @property
    def post(self):
        "Get the post value that is the result from the post refresh check."
        return self._post

    @post.setter
    def post(self, post):
        self._post = post

    @post.deleter
    def post(self):
        del self._post

    @property
    def assertion(self):
        "Get the assertion that is the result from the post refresh check."
        return self._assertion

    @assertion.setter
    def assertion(self, assertion):
        self._assertion = assertion

    @assertion.deleter
    def assertion(self):
        del self._assertion

    def _check(self, stage: str):
        """Runs the given function and stores results.
        Stored in either `self.pre` or `self.post` depending on `stage`.

        Args:
            stage (str): Either 'Pre' or 'Post'

        Returns:
            object: Returns the results of the pre or post check.
        """
        logger.debug(f"Running {stage}-Check for {self.name}")
        results = self.function()
        if stage == "Pre":
            self.pre = results
        else:
            self.post = results
        logger.info(f"{stage}-Check results for {self.name} - {results}")
        return results

    def pre_check(self):
        """Runs `self._check("Pre")`"""
        self._check("Pre")
        pass

    def post_check(self):
        """Runs `self._check("Post")` then `self.assertion_run()`"""
        self._check("Post")
        self.assertion_run()
        pass

    def assertion_run(self):
        """Runs the given self.assertion function with `self.pre` and `self.post`.
        So, `self.assertion_run(self.pre, self.post)`.
        """
        if self.assertion is None:
            logger.debug("Skipping assertion none given")
        else:
            test = self.assertion(self.pre, self.post)
            assert_str = f"Test {self.name} - {test} - Pre Results - {self.pre} | Post Results {self.post}"
            if test:
                logger.info(assert_str)
            else:
                logger.critical(assert_str)
            assert (
                test
            ), f"Test failed! Pre Results - {self.pre} | Post Results {self.post}"


class RefreshCheckCollection:
    """Groups together your `RefreshChecks` to handle multiple types of checks in a single refresh."""

    def __init__(self, refresh_checks: RefreshCheck = []) -> None:
        self._refreshchecks = refresh_checks
        pass

    def __iter__(self):
        """Basic iteration through the different `RefreshCheck`(s)."""
        for refresh_check in self._refreshchecks:
            yield refresh_check

    def add_refresh_check(self, refresh_check: RefreshCheck):
        """Add a RefreshCheck

        Args:
            RefreshCheck (RefreshCheck): `RefreshCheck` class.
        """
        self._refreshchecks.append(refresh_check)

    def remove_refresh_check(self, refresh_check: RefreshCheck):
        """Remove a RefreshCheck

        Args:
            RefreshCheck (RefreshCheck): `RefreshCheck` class.
        """
        self._refreshchecks.remove(refresh_check)

    def clear_refresh_checks(self):
        """Clear Refresh Checks."""
        self._refreshchecks.clear()


class PyRefresh:
    """PyRefresh Class to handle refreshes of model.

    Args:
        model (Tabular): Main Tabular Class
        object (Union[str, PyTable, PyPartition, Dict[str, Any]]): Designed to handle a few different ways of selecting a refresh. Can be a string of 'Table Name' or dict of {'Table Name': 'Partition Name'} or even some combination with the actual PyTable and PyPartition classes.
        trace (BaseTrace, optional): Set to `None` if no Tracing is desired, otherwise you can use default trace or create your own. Defaults to RefreshTrace.
        RefreshChecks (RefreshCheckCollection, optional): Add your `RefreshCheck`'s into a `RefreshCheckCollection`. Defaults to RefreshCheckCollection().
        default_row_count_check (bool, optional): Quick built in check will fail the refresh if post check row count is zero. Defaults to True.
        refresh_type (RefreshType, optional): Input RefreshType desired. Defaults to RefreshType.Full.
    """

    def __init__(
        self,
        model,
        object: Union[str, PyTable, PyPartition, Dict[str, Any]],
        trace: BaseTrace = RefreshTrace,
        refresh_checks: RefreshCheckCollection = RefreshCheckCollection(),
        default_row_count_check: bool = True,
        refresh_type: RefreshType = RefreshType.Full,
    ) -> None:
        self.model = model
        self.object = object
        self.trace = trace
        self.default_row_count_check = default_row_count_check
        self.refresh_type = refresh_type
        self._objects_to_refresh = []
        self._request_refresh(self.object)
        self._checks = refresh_checks
        self._pre_checks()
        logger.info("Refresh Request Completed!")
        pass

    def _pre_checks(self):
        """Checks if any `BaseTrace` classes are needed from `Tabular_Tracing.py`.
        Then checks if any `RefreshChecks` are needed, along with the default `Row_Count` check.
        """
        logger.debug("Running Pre-checks")
        if self.trace is not None:
            logger.debug("Getting Trace")
            self.trace = self._get_trace()
        if self.default_row_count_check:
            logger.debug(
                f"Running default row count check - {self.default_row_count_check}"
            )
            tables = [
                table
                for refresh_dict in self._objects_to_refresh
                for table in refresh_dict.keys()
            ]

            def row_count_assertion(pre, post):
                """Checks if table refreshed zero rows."""
                post = 0 if post is None else post
                return post > 0

            for table in set(tables):
                check = RefreshCheck(
                    f"{table.Name} Row Count", table.row_count, row_count_assertion
                )
                self._checks.add_refresh_check(check)
        for check in self._checks:
            check.pre_check()
        pass

    def _post_checks(self):
        """If traces are running it Stops and Drops it.
        Runs through any `post_checks()` in `RefreshChecks`.
        """
        if self.trace is not None:
            self.trace.stop()
            self.trace.drop()
        for check in self._checks:
            check.post_check()
            # self._checks.remove_refresh_check(check)
        self._checks.clear_refresh_checks()
        pass

    def _get_trace(self) -> BaseTrace:
        """Creates Trace and creates it in model."""
        return self.trace(self.model)

    def _find_table(self, table_str: str) -> Table:
        """Finds table in `PyTables` class."""
        try:
            result = self.model.Tables[table_str]
        except Exception:
            raise Exception(f"Unable to find table! from {table_str}")
        logger.debug(f"Found table {result.Name}")
        return result

    def _find_partition(self, table: Table, partition_str: str) -> Partition:
        """Finds partition in `PyPartitions` class."""
        try:
            result = table.Partitions[partition_str]
        except Exception:
            raise Exception(f"Unable to find partition! {table.Name}|{partition_str}")
        logger.debug(f"Found partition {result.Table.Name}|{result.Name}")
        return result

    def _refresh_table(self, table: PyTable) -> None:
        """Runs .Net `RequestRefresh()` on table."""
        logging.info(f"Requesting refresh for {table.Name}")
        self._objects_to_refresh += [
            {table: [partition for partition in table.Partitions]}
        ]
        table.RequestRefresh(self.refresh_type)

    def _refresh_partition(self, partition: PyPartition) -> None:
        """Runs .Net `RequestRefresh()` on partition."""
        logging.info(f"Requesting refresh for {partition.Table.Name}|{partition.Name}")
        self._objects_to_refresh += [{partition.Table: [partition]}]
        partition.RequestRefresh(self.refresh_type)

    def _refresh_dict(self, partition_dict: Dict) -> None:
        """Handles refreshes if argument given was a dictionary."""
        for table in partition_dict.keys():
            table_object = self._find_table(table) if isinstance(table, str) else table

            def handle_partitions(object):
                """
                Figures out if partition argument given is a str or an actual `PyPartition`.
                Then will run `self._refresh_partition()` appropriately.
                """
                if isinstance(object, str):
                    self._refresh_partition(self._find_partition(table_object, object))
                elif isinstance(object, PyPartition):
                    self._refresh_partition(object)
                else:
                    [handle_partitions(obj) for obj in object]

            handle_partitions(partition_dict[table])

    def _request_refresh(self, object):
        """Base method to parse through argument and figure out what needs to be refreshed. Someone please make this better..."""
        logger.debug(f"Requesting Refresh for {object}")
        if isinstance(object, str):
            self._refresh_table(self._find_table(object))
        elif isinstance(object, PyTables):
            [self._refresh_table(table) for table in object]
        elif isinstance(object, Dict):
            self._refresh_dict(object)
        elif isinstance(object, PyTable):
            self._refresh_table(object)
        elif isinstance(object, PyPartition):
            self._refresh_partition(object)
        else:
            [self._request_refresh(obj) for obj in object]

    def _refresh_report(self, property_changes) -> pd.DataFrame:
        """Builds a DataFrame that displays details on the refresh.

        Args:
            Property_Changes: Which is returned from `model.SaveChanges()`

        Returns:
            pd.DataFrame: DataFrame of refresh details.
        """
        logger.debug("Running Refresh Report...")
        refresh_data = []
        for property_change in property_changes:
            if (
                isinstance(property_change.object, Partition)
                and property_change.property_name == "RefreshedTime"
            ):
                table, partition, refreshed_time = (
                    property_change.object.Table.Name,
                    property_change.object.Name,
                    ticks_to_datetime(property_change.new_value.Ticks),
                )
                logger.info(
                    f'{table} - {partition} Refreshed! - {refreshed_time.strftime("%m/%d/%Y, %H:%M:%S")}'
                )
                refresh_data += [[table, partition, refreshed_time]]
        return pd.DataFrame(
            refresh_data, columns=["Table", "Partition", "Refreshed Time"]
        )

    def run(self) -> pd.DataFrame:
        """Brings it all together. When ready, executes all the pre checks.
        Then refreshes. Then runs all the post checks.
        """
        if self.model.Server.Connected is False:
            logger.info(f"{self.Server.Name} - Reconnecting...")
            self.model.recconect()

        if self.trace is not None:
            self.trace.start()

        save_changes = self.model.save_changes()

        self._post_checks()

        return self._refresh_report(save_changes.property_changes)
