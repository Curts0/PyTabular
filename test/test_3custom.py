"""These are tests I have for pretty janky features of PyTabular.
These were designed selfishly for my own uses.
So seperating out, to one day sunset and remove.
"""
from test.config import testing_parameters, testingtablename
import pytest


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
