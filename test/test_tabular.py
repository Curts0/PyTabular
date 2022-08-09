from pytabular import pytabular
from pytabular import localsecret
import clr
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular.json')
clr.AddReference('Microsoft.AnalysisServices')
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection
from Microsoft.AnalysisServices.Tabular import Server, Database, RefreshType, ConnectionDetails, ColumnType
from Microsoft.AnalysisServices import UpdateOptions
aas = pytabular.Tabular(localsecret.CONNECTION_STR['FIN 500'])
gen2 = pytabular.Tabular(localsecret.CONNECTION_STR['GEN2TEST'])

def test_connection():
	'''
	Does a quick check to the Tabular Class
	To ensure that it can connnect
	'''
	assert aas.Server.Connected and gen2.Server.Connected

def test_database():
	assert isinstance(aas.Database,Database) and isinstance(aas.Database,Database)

def test_query():
	'''
	Does a quick query on the model and checks if it will return expected value
	'''
	df_aas = aas.Query('EVALUATE {1}')
	df_gen2 = gen2.Query('EVALUATE {1}')
	assert df_aas.iloc[0]['[Value]'] == 1 and df_gen2.iloc[0]['[Value]'] == 1

def test_bpa():
	'''
	BPA Tests
	'''
	te2 = pytabular.TE2().EXE_Path
	bpa = pytabular.BPA().Location
	assert aas.Analyze_BPA(te2,bpa) and gen2.Analyze_BPA(te2,bpa)
