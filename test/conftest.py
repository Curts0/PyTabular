"""pytest conftest.py.

Has a `TestingStorage()` class to pass parameters from one test to another.
This file also has functions that give instructions on start and finish of pytest.
See `config.py` for more testing configurations.
"""

from test.config import (
    local_pbix,
    testingtablename,
    testingtabledf,
)
import pytabular as p


class TestStorage:
    """Class to pass parameters from on pytest to another."""

    query_trace = None
    documentation_class = None


def pytest_report_header(config):
    """Pytest header name."""
    return "PyTabular Local Testing"


def remove_testing_table(model):
    """Function to remove the testing table."""
    table_check = [
        table
        for table in model.Model.Tables.GetEnumerator()
        if testingtablename in table.Name
    ]
    for table in table_check:
        p.logger.info(f"Removing table {table.Name} from {model.Server.Name}")
        model.Model.Tables.Remove(table)
    model.SaveChanges()

def pytest_generate_tests(metafunc):
    if "model" in metafunc.fixturenames:
        metafunc.parametrize("model", [local_pbix], ids=[local_pbix.Name])

def pytest_sessionstart(session):
    """Run at pytest start.

    Removes testing table if exists, and creates a new one.
    """
    p.logger.info("Executing pytest setup...")
    remove_testing_table(local_pbix)
    local_pbix.create_table(testingtabledf, testingtablename)
    return True


def pytest_sessionfinish(session, exitstatus):
    """On pytest finish it will remove testing table."""
    p.logger.info("Executing pytest cleanup...")
    remove_testing_table(local_pbix)
    # p.logger.info("Finding and closing PBIX file...")
    # subprocess.run(["powershell", "Stop-Process -Name PBIDesktop"])
    return True
