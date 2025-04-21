"""pytest for bpa."""

import pytest
import pytabular as p
from test.config import testing_parameters
from os import getcwd


def test_bpa(model):
    """Testing execution of `model.analyze_bpa()`."""
    te2 = p.TabularEditor(verify_download=False).exe
    bpa = p.BPA(verify_download=False).location
    assert isinstance(model.analyze_bpa(te2, bpa), list)


def test_te2_custom_file_path(model):
    """Testing TE2 Class."""
    assert isinstance(p.TabularEditor(getcwd()), p.TabularEditor)


def test_bpa_custom_file_path(model):
    """Testing BPA Class."""
    assert isinstance(p.BPA(getcwd()), p.BPA)
