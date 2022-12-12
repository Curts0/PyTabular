from test.config import aas, gen2, testingtablename, testingtabledf
import pytabular as p


def pytest_report_header(config):
    return "PyTabular Local Testing"


def remove_testing_table(model):
    table_check = [
        table
        for table in model.Model.Tables.GetEnumerator()
        if testingtablename in table.Name
    ]
    for table in table_check:
        model.Model.Tables.Remove(table)
    model.SaveChanges()


def pytest_sessionstart(session):
    p.logger.info("Executing pytest setup...")
    remove_testing_table(aas)
    remove_testing_table(gen2)
    aas.Create_Table(testingtabledf, testingtablename)
    gen2.Create_Table(testingtabledf, testingtablename)
    return True


def pytest_sessionfinish(session, exitstatus):
    p.logger.info("Executing pytest cleanup...")
    remove_testing_table(aas)
    remove_testing_table(gen2)
    return True
