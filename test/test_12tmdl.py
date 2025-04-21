import pytabular as p
from test.conftest import TestStorage
from test.config import testing_parameters
import pytest

path = "tmdl_testing"

@pytest.mark.parametrize("model", testing_parameters)
def test_tmdl_save(model):
    """Tests basic tmdl save to folder functionality."""
    stf = p.Tmdl(model).save_to_folder(path)
    assert stf

@pytest.mark.parametrize("model", testing_parameters)
def test_tmdl_execute(model):
    """Tests basic tmdl execute functionality."""
    exec = p.Tmdl(model).execute(path, False)
    p.logic_utils.remove_folder_and_contents(path)
    assert exec