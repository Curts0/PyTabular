import pytabular as p
import local
import pandas as pd
import pytest

PLACEHOLDER_AAS = local.AAS
PLACEHOLDER_GEN2 = local.GEN2
aas = p.Tabular(PLACEHOLDER_AAS)
gen2 = p.Tabular(PLACEHOLDER_GEN2)
testingtablename = "PyTestTable"
testingtabledf = pd.DataFrame(data={"col1": [1, 2, 3], "col2": ["four", "five", "six"]})
testing_parameters = [pytest.param(aas, id="AAS"), pytest.param(gen2, id="GEN2")]
