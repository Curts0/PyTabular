from tabular_tracing import Refresh_Trace
import logging
from Microsoft.AnalysisServices.Tabular import (
    RefreshType,
    Table,
    Partition,
)
import pandas as pd
from logic_utils import ticks_to_datetime
from typing import Union, Dict, Any, Iterable
from table import PyTable
from partition import PyPartition


logger = logging.getLogger("PyTabular")


class PyRefresh:
    def __init__(
        self,
        model,
        object: Union[str, Table, Partition, Dict[str, Any]],
        tracing: bool =True,
        row_count_check: bool =True,
        refresh_type: RefreshType =RefreshType.Full,
    ) -> None:
        self.model = model
        self.object = object
        self.tracing = tracing
        self.row_count_check = row_count_check
        self.refresh_type = refresh_type
        self._objects_to_refresh = []
        self._request_refresh(self.object)
        self._pre_checks()
        logger.info("Refresh Request Completed!")
        pass

    def _pre_checks(self):
        if self.tracing:
            self.trace = self._get_trace()
        if self.row_count_check:
            self._pre_row_counts = {}
            tables = [table for refresh_dict in self._objects_to_refresh for table in refresh_dict.keys()]
            for table in set(tables):
                self._pre_row_counts[table.Name] = table.Row_Count()
                logger.debug(f"{table.Name} Pre Refresh Row Count - {str(self._pre_row_counts[table.Name])}")
        return 1

    def _get_trace(self) -> Refresh_Trace:
        return Refresh_Trace(self.model)

    def _find_table(self, table_str: str) -> Table:
        try:
            result = self.model.Tables[table_str]
        except Exception:
            raise Exception(f"Unable to find table! from {table_str}")
        logger.debug(f"Found table {result.Name}")
        return result

    def _find_partition(self, table: Table, partition_str: str) -> Partition:
        try:
            result = table.Partitions[partition_str]
        except Exception:
            raise Exception(f"Unable to find partition! {table.Name}|{partition_str}")
        logger.debug(f"Found partition {result.Table.Name}|{result.Name}")
        return result

    def _refresh_table(self, table: PyTable) -> None:
        logging.info(f"Requesting refresh for {table.Name}")
        self._objects_to_refresh += [{table: [partition for partition in table.Partitions]}]
        table.RequestRefresh(self.refresh_type)

    def _refresh_partition(self, partition: PyPartition) -> None:
        logging.info(f"Requesting refresh for {partition.Table.Name}|{partition.Name}")
        self._objects_to_refresh += [{partition.Table: [partition]}]
        partition.RequestRefresh(self.refresh_type)

    def _refresh_dict(self, partition_dict: Dict) -> None:
        for table in partition_dict.keys():
            table_object = self._find_table(table) if isinstance(table, str) else table

            def handle_partitions(object):
                if isinstance(object, str):
                    self._refresh_partition(self._find_partition(table_object, object))
                elif isinstance(object, PyPartition):
                    self._refresh_partition(object)
                else:
                    [handle_partitions(obj) for obj in object]

            handle_partitions(partition_dict[table])

    def _request_refresh(self, object):
        logger.debug(f'Requesting Refresh for {object}')
        if isinstance(object, str):
            self._refresh_table(self._find_table(object))
        elif isinstance(object, Dict):
            self._refresh_dict(object)
        elif isinstance(object, PyTable):
            self._refresh_table(object)
        elif isinstance(object, PyPartition):
            self._refresh_partition(object)
        else:
            [self._request_refresh(obj) for obj in object]

    def _refresh_report(self, Property_Changes) -> pd.DataFrame:
        logger.debug("Running Refresh Report...")
        refresh_data = []
        for property_change in Property_Changes:
            if (
                isinstance(property_change.Object, Partition)
                and property_change.Property_Name == "RefreshedTime"
            ):
                table, partition, refreshed_time = (
                    property_change.Object.Table.Name,
                    property_change.Object.Name,
                    ticks_to_datetime(property_change.New_Value.Ticks),
                )
                logger.info(
                    f'{table} - {partition} Refreshed! - {refreshed_time.strftime("%m/%d/%Y, %H:%M:%S")}'
                )
                refresh_data += [[table, partition, refreshed_time]]
        return pd.DataFrame(
            refresh_data, columns=["Table", "Partition", "Refreshed Time"]
        )

    def Run(self) -> None:
        if not self.model.Server.Connected:
            logger.info(f"{self.Server.Name} - Reconnecting...")
            self.model.Server.Reconnect()

        if self.tracing:
            self.trace.Start()

        save_changes = self.model.SaveChanges()

        if self.tracing:
            self.trace.Stop()
            self.trace.Drop()

        return self._refresh_report(save_changes.Property_Changes)
