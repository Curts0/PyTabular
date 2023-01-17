"""These are tests I have for pretty janky features of PyTabular.
These were designed selfishly for my own uses.
So seperating out, to one day sunset and remove.
"""
from test.config import testing_parameters, testingtablename
import pytest
import pytabular as p
import pandas as pd


@pytest.mark.parametrize("model", testing_parameters)
def test_backingup_table(model):
    model.Backup_Table(testingtablename)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if f"{testingtablename}_backup" == table.Name
            ]
        )
        == 1
    )


@pytest.mark.parametrize("model", testing_parameters)
def test_revert_table2(model):
    model.Revert_Table(testingtablename)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if f"{testingtablename}" == table.Name
            ]
        )
        == 1
    )


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_table_deprecate(model):
    assert len(model.Query_Every_Table()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_column_deprecate(model):
    assert len(model.Query_Every_Column()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_zero_row_tables_deprecate(model):
    assert isinstance(p.Return_Zero_Row_Tables(model), list)


@pytest.mark.parametrize("model", testing_parameters)
def test_last_refresh_times_deprecate(model):
    assert isinstance(p.Table_Last_Refresh_Times(model), pd.DataFrame)
