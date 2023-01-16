from test.config import (
    local_pbix,
    testingtablename,
    testingtabledf,
)
import pytabular as p
import subprocess


class testing_storage:
    query_trace = None


def pytest_report_header(config):
    return "PyTabular Local Testing"


def remove_testing_table(model):
    table_check = [
        table
        for table in model.Model.Tables.GetEnumerator()
        if testingtablename in table.Name
    ]
    for table in table_check:
        p.logger.info(f"Removing table {table.Name} from {model.Server.Name}")
        model.Model.Tables.Remove(table)
    model.SaveChanges()


def pytest_sessionstart(session):
    p.logger.info("Executing pytest setup...")
    remove_testing_table(local_pbix)
    local_pbix.Create_Table(testingtabledf, testingtablename)
    return True


def pytest_sessionfinish(session, exitstatus):
    p.logger.info("Executing pytest cleanup...")
    remove_testing_table(local_pbix)
    p.logger.info("Finding and closing PBIX file...")
    subprocess.run(["powershell", "Stop-Process -Name PBIDesktop"])
    return True
