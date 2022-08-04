import datetime
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')

def ticks_to_datetime(ticks:int) -> datetime.datetime:
	'''
	Converts a C# System DateTime Tick into a Python DateTime
	https://gist.github.com/gamesbook/03d030b7b79370fb6b2a67163a8ac3b5
	https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0
	Example: 637922723630700000 -> datetime.datetime(2022, 7, 1, 11, 39, 23, 70000)
	'''
	return datetime.datetime(1,1,1) + datetime.timedelta(microseconds=ticks//10)

def pd_dataframe_to_dax_expression(df:pd.DataFrame) -> str:
	'''
	This will take a pandas dataframe and convert to a dax expression
	For example this DF:
		col1  col2
	0   1     3
	1   2     4

	|
	|
	V

	Will convert to this expression string:
	DEFINE
		TABLE tablename = { ( 1, 3 ), ( 2, 4 ) }

	EVALUATE
	SELECTCOLUMNS(
		tablename,
		"col1", tablename[Value1],
		"col2", tablename[Value2]
	)
	'''
	return True
def pd_dataframe_to_m_expression(df:pd.DataFrame) -> str:
	'''
	This will take a pandas dataframe and convert to an m expression
	For example this DF:
	   col1  col2
	0   1     3
	1   2     4
	
	|
	|
	V

	Will convert to this expression string:
	let
	Source=#table({"col1","col2"},
	{
	{"1","3"},{"2","4"}
	})
	in
	Source
	'''
	def m_list_expression_generator(list_of_strings: list[str]) -> str:
		'''
		Takes a python list of strings and converts to power query m expression list format...
		Ex: ["item1","item2","item3"] --> {"item1","item2","item3"}
		Codepoint reference --> \u007b == { and \u007d == }
		'''
		string_components = ','.join([f'\"{string_value}\"' for string_value in list_of_strings])
		return f'\u007b{string_components}\u007d'
	logging.debug(f'Executing m_list_generator()... for {df.columns}')
	columns = m_list_expression_generator(df.columns)
	expression_str = f"let\nSource=#table({columns},\n"
	logging.debug(f'Iterating through rows to build expression... df has {len(df)} rows...')
	expression_list_rows = []
	for index, row in df.iterrows():
		expression_list_rows += [m_list_expression_generator(row.to_list())]
	expression_str += f"\u007b\n{','.join(expression_list_rows)}\n\u007d)\nin\nSource"
	return expression_str