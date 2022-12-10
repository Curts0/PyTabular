import local
import pytest
import pandas as pd
from test.config import testingtablename, testing_parameters


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
    singlevaltest = local.SINGLEVALTESTPATH
    dfvaltest = local.DFVALTESTPATH
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
