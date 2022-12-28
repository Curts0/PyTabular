import pytest
import pytabular as p
from test.config import testing_parameters


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa(model):
    te2 = p.Tabular_Editor().EXE
    bpa = p.BPA().Location
    assert isinstance(model.Analyze_BPA(te2, bpa), list)
