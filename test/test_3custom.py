"""These are tests I have for pretty janky features of PyTabular.
These were designed selfishly for my own uses.
So seperating out, to one day sunset and remove.
"""
from test.config import aas, gen2, testingtablename
import pytest

testing_parameters = [pytest.param(aas, id="AAS"), pytest.param(gen2, id="GEN2")]


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_table(model):
    assert len(model.Query_Every_Table()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_column(model):
    assert len(model.Query_Every_Column()) > 0


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
def test_revert_table(model):
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
