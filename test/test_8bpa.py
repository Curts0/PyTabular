import pytest
import pytabular as p
from test.config import testing_parameters
from os import getcwd


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa(model):
    te2 = p.TabularEditor().exe
    bpa = p.BPA().location
    assert isinstance(model.analyze_bpa(te2, bpa), list)


@pytest.mark.parametrize("model", testing_parameters)
def test_te2_custom_file_path(model):
    assert isinstance(p.TabularEditor(getcwd()), p.TabularEditor)


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa_custom_file_path(model):
    assert isinstance(p.BPA(getcwd()), p.BPA)
