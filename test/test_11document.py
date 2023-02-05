"""Tests to cover the document.py file
"""
from test.config import testing_parameters
import pytest
import pytabular as p
import os
from pytabular import logic_utils
from test.conftest import TestStorage


@pytest.mark.parametrize("model", testing_parameters)
def test_basic_document_funcionality(model):
    try:
        docs = p.ModelDocumenter(model=model)
        docs.generate_documentation_pages()
        docs.save_documentation()
        TestStorage.documentation_class = docs
    except Exception:
        pytest.fail("Unsuccessful documentation generation..")


def test_basic_documentation_removed():
    docs_class = TestStorage.documentation_class
    remove = f"{docs_class.save_location}/{docs_class.friendly_name}"
    logic_utils.remove_folder_and_contents(remove)
    assert os.path.exists(remove) is False
