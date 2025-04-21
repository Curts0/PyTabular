"""Tests to cover the tmdl.py file."""

import pytabular as p

path = "tmdl_testing"


def test_tmdl_save(model):
    """Tests basic tmdl save to folder functionality."""
    stf = p.Tmdl(model).save_to_folder(path)
    assert stf


def test_tmdl_execute(model):
    """Tests basic tmdl execute functionality."""
    exec = p.Tmdl(model).execute(path, False)
    p.logic_utils.remove_folder_and_contents(path)
    assert exec
