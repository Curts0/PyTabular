from pytabular import pytabular
from pytabular import localsecret
tab = pytabular.Tabular(localsecret.CONNECTION_STR['FIN 300'])
'''
def test_query_all_tables():
	assert len(tab.Query_Every_Column()) > 0
'''