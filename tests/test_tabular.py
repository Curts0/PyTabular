from pybi import tabular
def test_connection():
	'''
	Does a quick check to the Tabular Class
	To ensure that it can connnect
	'''
	assert tabular.Tabular().Server.Connected

