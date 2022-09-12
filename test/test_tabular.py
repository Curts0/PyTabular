import pytabular
import local as l
import pytest
import pandas as pd
from Microsoft.AnalysisServices.Tabular import Database

aas = pytabular.Tabular(l.AAS)
gen2 = pytabular.Tabular(l.GEN2)
testing_parameters = [(aas),(gen2)]
testingtable = 'PyTestTable'

@pytest.mark.parametrize("model",testing_parameters)
def test_connection(model):
	'''
	Does a quick check to the Tabular Class
	To ensure that it can connnect
	'''
	assert model.Server.Connected

@pytest.mark.parametrize("model",testing_parameters)
def test_database(model):
	assert isinstance(model.Database,Database)

@pytest.mark.parametrize("model",testing_parameters)
def test_query(model):
	int_result = model.Query('EVALUATE {1}')
	text_result = model.Query('EVALUATE {"Hello World"}')
	assert int_result == 1 and text_result == 'Hello World'


def remove_testing_table(model):
	table_check = [table for table in model.Model.Tables.GetEnumerator() if testingtable in table.Name]
	for table in table_check:
		model.Model.Tables.Remove(table)
	model.SaveChanges()

@pytest.mark.parametrize("model",testing_parameters)
def test_pre_table_checks(model):
	remove_testing_table(model)
	assert len([table for table in model.Model.Tables.GetEnumerator()  if testingtable in table.Name]) == 0

@pytest.mark.parametrize("model",testing_parameters)
def test_create_table(model):
	df = pd.DataFrame(data={'col1':[1,2,3],'col2':['four','five','six']})
	model.Create_Table(df,testingtable)
	assert len(model.Query(f"EVALUATE {testingtable}")) == 3

@pytest.mark.parametrize("model",testing_parameters)
def test_backingup_table(model):
	model.Backup_Table(testingtable)
	assert len([table for table in model.Model.Tables.GetEnumerator()  if f'{testingtable}_backup' == table.Name]) == 1

@pytest.mark.parametrize("model",testing_parameters)
def test_revert_table(model):
	model.Revert_Table(testingtable)
	assert len([table for table in model.Model.Tables.GetEnumerator()  if f'{testingtable}' == table.Name]) == 1


@pytest.mark.parametrize("model",testing_parameters)
def test_table_removal(model):
	remove_testing_table(model)
	assert len([table for table in model.Model.Tables.GetEnumerator()  if testingtable in table.Name]) == 0

@pytest.mark.parametrize("model",testing_parameters)
def test_bpa(model):
	te2 = pytabular.Tabular_Editor().EXE
	bpa = pytabular.BPA().Location
	assert model.Analyze_BPA(te2,bpa) 
