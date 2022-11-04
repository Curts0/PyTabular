import pytabular
import local
import pytest
import pandas as pd
from Microsoft.AnalysisServices.Tabular import Database

aas = pytabular.Tabular(local.AAS)
gen2 = pytabular.Tabular(local.GEN2)
testing_parameters = [(aas), (gen2)]
testingtablename = "PyTestTable"
testingtabledf = pd.DataFrame(data={"col1": [1, 2, 3], "col2": ["four", "five", "six"]})


@pytest.mark.parametrize("model", testing_parameters)
def test_sanity_check(model):
    assert 1 == 1


@pytest.mark.parametrize("model", testing_parameters)
def test_connection(model):
    """
    Does a quick check to the Tabular Class
    To ensure that it can connnect
    """
    assert model.Server.Connected


@pytest.mark.parametrize("model", testing_parameters)
def test_database(model):
    assert isinstance(model.Database, Database)


@pytest.mark.parametrize("model", testing_parameters)
def test_basic_query(model):
    int_result = model.Query("EVALUATE {1}")
    text_result = model.Query('EVALUATE {"Hello World"}')
    assert int_result == 1 and text_result == "Hello World"


@pytest.mark.parametrize("model", testing_parameters)
def test_file_query(model):
    singlevaltest = local.SINGLEVALTESTPATH
    dfvaltest = local.DFVALTESTPATH
    dfdupe = pd.DataFrame({"[Value1]": (1, 3), "[Value2]": (2, 4)})
    assert model.Query(singlevaltest) == 1 and model.Query(dfvaltest).equals(dfdupe)


@pytest.mark.parametrize("model", testing_parameters)
def test_repr_str(model):
    assert isinstance(model.__repr__(), str)


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_table(model):
    assert len(model.Query_Every_Table()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_query_every_column(model):
    assert len(model.Query_Every_Column()) > 0


def remove_testing_table(model):
    table_check = [
        table
        for table in model.Model.Tables.GetEnumerator()
        if testingtablename in table.Name
    ]
    for table in table_check:
        model.Model.Tables.Remove(table)
    model.SaveChanges()


@pytest.mark.parametrize("model", testing_parameters)
def test_pre_table_checks(model):
    remove_testing_table(model)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if testingtablename in table.Name
            ]
        )
        == 0
    )


@pytest.mark.parametrize("model", testing_parameters)
def test_create_table(model):
    df = pd.DataFrame(data={"col1": [1, 2, 3], "col2": ["four", "five", "six"]})
    model.Create_Table(df, testingtablename)
    assert len(model.Query(f"EVALUATE {testingtablename}")) == 3


@pytest.mark.parametrize("model", testing_parameters)
def test_pytables_count(model):
    assert model.Tables[testingtablename].Row_Count() > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_pytables_refresh(model):
    assert model.Tables[testingtablename].Refresh()


@pytest.mark.parametrize("model", testing_parameters)
def test_pypartitions_refresh(model):
    assert model.Tables[testingtablename].Partitions[0].Refresh()


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
def test_table_removal(model):
    remove_testing_table(model)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if testingtablename in table.Name
            ]
        )
        == 0
    )


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa(model):
    te2 = pytabular.Tabular_Editor().EXE
    bpa = pytabular.BPA().Location
    assert isinstance(model.Analyze_BPA(te2, bpa), list)
