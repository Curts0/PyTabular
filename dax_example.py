from sys import path
path.append('C:\\Program Files (x86)\\Microsoft.NET\\ADOMD.NET\\130')

from pyadomd import Pyadomd

conn_str = "Data Source=asazure://centralus.asazure.windows.net/azraasdaientdlfn700;Initial Catalog=FINANCE;Cube=Model;User ID=svc-azssas-process-p@rockwellautomation.com;Password=');!3xk3YlB(Fatf'"
query = """EVALUATE TOPN(5,FACT_COPA)"""

with Pyadomd(conn_str) as conn:
	with conn.cursor().execute(query) as cur:
		print(cur.fetchall())
from pandas import DataFrame
with Pyadomd(conn_str) as conn:
	with conn.cursor().execute(query) as cur:
		df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
		print(df)