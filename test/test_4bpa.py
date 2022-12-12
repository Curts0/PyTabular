from test.config import aas, gen2
import pytest
import pytabular as p

testing_parameters = [pytest.param(aas, id="AAS"), pytest.param(gen2, id="GEN2")]


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa(model):
    te2 = p.Tabular_Editor().EXE
    bpa = p.BPA().Location
    assert isinstance(model.Analyze_BPA(te2, bpa), list)
