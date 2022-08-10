from pytabular import pytabular
from pytabular import localsecret
import pytest
import pandas as pd
from Microsoft.AnalysisServices.Tabular import Database

aas = pytabular.Tabular(localsecret.CONNECTION_STR['FIN 500'])
gen2 = pytabular.Tabular(localsecret.CONNECTION_STR['GEN2TEST'])
testingtable = 'PyTestTable'
pytestmark = pytest.mark.parametrize("model",[(aas),(gen2)])

def test_connection(model):
	'''
	Does a quick check to the Tabular Class
	To ensure that it can connnect
	'''
	assert model.Server.Connected

def test_database(model):
	assert isinstance(model.Database,Database)

def test_query(model):
	'''
	Does a quick query on the model and checks if it will return expected value
	'''
	df = model.Query('EVALUATE {1}')
	assert df.iloc[0]['[Value]'] == 1

def remove_py_tables(model):
	table_check = [table for table in model.Tables if testingtable in table.Name]
	try:
		for table in table_check:
			model.Model.Tables.Remove(table)
		model.Update()
		return True
	except:
		return False

def test_pre_table_checks(model):
	assert remove_py_tables(model)

def test_create_table(model):
	df = pd.DataFrame(data={'col1':[1,2,3],'col2':['four','five','six']})
	assert model.Create_Table(df,testingtable)

def test_backingup_table(model):
	assert model.Backup_Table(testingtable)

def test_revert_table(model):
	assert model.Revert_Table(testingtable)

def test_table_removal(model):
	assert remove_py_tables(model)

def test_bpa(model):
	te2 = pytabular.TE2().EXE_Path
	bpa = pytabular.BPA().Location
	assert model.Analyze_BPA(te2,bpa)