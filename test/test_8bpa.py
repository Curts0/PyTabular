import pytest
import pytabular as p
from test.config import testing_parameters
from os import getcwd
import pandas as pd


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa(model):
    te2 = p.Tabular_Editor().EXE
    bpa = p.BPA().Location
    assert isinstance(model.Analyze_BPA(te2, bpa), list)


@pytest.mark.parametrize("model", testing_parameters)
def test_te2_custom_file_path(model):
    assert isinstance(p.Tabular_Editor(getcwd()), p.Tabular_Editor)


@pytest.mark.parametrize("model", testing_parameters)
def test_bpa_custom_file_path(model):
    assert isinstance(p.BPA(getcwd()), p.BPA)
