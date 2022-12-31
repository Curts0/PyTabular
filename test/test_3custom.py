"""These are tests I have for pretty janky features of PyTabular.
These were designed selfishly for my own uses.
So seperating out, to one day sunset and remove.
"""
from test.config import testing_parameters, testingtablename, LOCAL_FILE
import pytest


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


@pytest.mark.parametrize("model", testing_parameters)
def test_get_dependencies(model):
    if len(model.Measures) > 0:
        dependencies = model.Measures[0].get_dependencies()
        assert len(dependencies) > 0
    else:
        assert True


@pytest.mark.parametrize("model", testing_parameters)
def test_get_sample_values(model):
    if LOCAL_FILE[0] == "AdventureWorks Sales":
        df = model.Columns["Country"].get_sample_values()
        assert len(df) > 0
    else:
        assert True
