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
tab = pytabular.Tabular(localsecret.CONNECTION_STR['FIN 500'])

def test_connection():
	'''
	Does a quick check to the Tabular Class
	To ensure that it can connnect
	'''
	assert tab.Server.Connected

def test_database():
	assert isinstance(tab.Database,Database)

def test_query():
	'''
	Does a quick query on the model and checks if it will return expected value
	'''
	df = tab.Query('EVALUATE {1}')
	assert df.iloc[0]['[Value]'] == 1

tab.Disconnect()
