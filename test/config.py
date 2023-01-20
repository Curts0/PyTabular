import pytabular as p
import os
import pandas as pd
import pytest
import subprocess
from time import sleep


def get_test_path():
    cwd = os.getcwd()
    if os.path.basename(cwd) == "test":
        return cwd
    elif "test" in os.listdir():
        return cwd + "\\test"
    else:
        raise BaseException("Unable to find test path...")


adventureworks_path = f'"{get_test_path()}\\adventureworks\\AdventureWorks Sales.pbix"'


def find_local_pbi():
    attempt = p.find_local_pbi_instances()
    if len(attempt) > 0:
        return attempt[0]
    else:
        p.logger.info(f"Opening {adventureworks_path}")
        subprocess.run(["powershell", f"Start-Process {adventureworks_path}"])
        # Got to be a better way to wait and ensure the PBIX file is open?
        p.logger.info("sleep(30)... Need a better way to wait until PBIX is loaded...")
        sleep(30)
        return p.find_local_pbi_instances()[0]


LOCAL_FILE = find_local_pbi()

p.logger.info(f"Connecting to... {LOCAL_FILE[0]} - {LOCAL_FILE[1]}")
local_pbix = p.Tabular(LOCAL_FILE[1])


p.logger.info("Generating test data...")
testingtablename = "PyTestTable"
testingtabledf = pd.DataFrame(data={"col1": [1, 2, 3], "col2": ["four", "five", "six"]})
testing_parameters = [
    pytest.param(local_pbix, id=local_pbix.Name),
]
