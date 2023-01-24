import pytest
import pandas as pd
import pytabular as p
from test.config import testingtablename, testing_parameters, get_test_path


@pytest.mark.parametrize("model", testing_parameters)
def test_basic_query(model):
    int_result = model.Query("EVALUATE {1}")
    text_result = model.Query('EVALUATE {"Hello World"}')
    assert int_result == 1 and text_result == "Hello World"


datatype_queries = [
    ["this is a string", '"this is a string"'],
    [1, 1],
    [1000.78, "CONVERT(1000.78,CURRENCY)"],
]


@pytest.mark.parametrize("model", testing_parameters)
def test_datatype_query(model):
    for query in datatype_queries:
        result = model.Query(f"EVALUATE {{{query[1]}}}")
        assert result == query[0]


@pytest.mark.parametrize("model", testing_parameters)
def test_file_query(model):
    singlevaltest = get_test_path() + "\\singlevaltest.dax"
    dfvaltest = get_test_path() + "\\dfvaltest.dax"
    dfdupe = pd.DataFrame({"[Value1]": (1, 3), "[Value2]": (2, 4)})
    assert model.Query(singlevaltest) == 1 and model.Query(dfvaltest).equals(dfdupe)


@pytest.mark.parametrize("model", testing_parameters)
def test_repr_str(model):
    assert isinstance(model.__repr__(), str)


@pytest.mark.parametrize("model", testing_parameters)
def test_pytables_count(model):
    assert model.Tables[testingtablename].Row_Count() > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_pytables_refresh(model):
    assert len(model.Tables[testingtablename].Refresh()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_pypartitions_refresh(model):
    assert len(model.Tables[testingtablename].Partitions[0].Refresh()) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_pyobjects_adding(model):
    table = model.Tables.Find(testingtablename)
    table += table
    assert len(table) == 2


@pytest.mark.parametrize("model", testing_parameters)
def test_nonetype_decimal_bug(model):
    query_str = """
    EVALUATE
    {
        (1, CONVERT( 1.24, CURRENCY ), "Hello"), (2, CONVERT( 87661, CURRENCY ), "World"), (3,,"Test")
    }
    """
    assert len(model.Query(query_str)) == 3


@pytest.mark.parametrize("model", testing_parameters)
def test_Table_Last_Refresh_Times(model):
    """Really just testing the the function completes successfully and returns df"""
    assert isinstance(model.Tables.Last_Refresh(), pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_Return_Zero_Row_Tables(model):
    """Testing that `Return_Zero_Row_Tables`"""
    assert isinstance(model.Tables.Find_Zero_Rows(), p.pytabular.PyTables)


@pytest.mark.parametrize("model", testing_parameters)
def test_get_dependencies(model):
    dependencies = model.Measures[0].get_dependencies()
    assert len(dependencies) > 0


@pytest.mark.parametrize("model", testing_parameters)
def test_disconnect(model):
    """Tests `Disconnect()` from `Tabular` class."""
    model.Disconnect()
    assert model.Server.Connected is False


@pytest.mark.parametrize("model", testing_parameters)
def test_reconnect(model):
    """Tests `Reconnect()` from `Tabular` class."""
    model.Reconnect()
    assert model.Server.Connected is True


@pytest.mark.parametrize("model", testing_parameters)
def test_reconnect_savechanges(model):
    """This will test the `Reconnect()` gets called in `SaveChanges()`"""
    model.Disconnect()
    model.SaveChanges()
    assert model.Server.Connected is True


@pytest.mark.parametrize("model", testing_parameters)
def test_is_process(model):
    """Checks that `Is_Process()` from `Tabular` class returns bool"""
    assert isinstance(model.Is_Process(), bool)


@pytest.mark.parametrize("model", testing_parameters)
def test_bad_table(model):
    """Checks for unable to find table exception"""
    with pytest.raises(Exception):
        model.Refresh("badtablename")


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh_dict(model):
    """Checks for refreshing dictionary"""
    table = model.Tables[testingtablename]
    refresh = model.Refresh({table.Name: table.Partitions[0].Name})
    assert isinstance(refresh, pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_refresh_dict_pypartition(model):
    """Checks for refreshing dictionary"""
    table = model.Tables[testingtablename]
    refresh = model.Refresh({table.Name: table.Partitions[0]})
    assert isinstance(refresh, pd.DataFrame)


@pytest.mark.parametrize("model", testing_parameters)
def test_bad_partition(model):
    """Checks for refreshing dictionary"""
    table = model.Tables[testingtablename]
    with pytest.raises(Exception):
        model.Refresh({table.Name: table.Partitions[0].Name + "fail"})
