import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')

import datetime
from typing import Dict
import pandas as pd

import clr
clr.AddReference('Microsoft.AnalysisServices.Tabular')
from Microsoft.AnalysisServices.Tabular import DataType

def ticks_to_datetime(ticks:int) -> datetime.datetime:
	'''Converts a C# System DateTime Tick into a Python DateTime

	Args:
		ticks (int): (C# DateTime Tick)[https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks?view=net-6.0]

	Returns:
		datetime.datetime: datetime.datetime value
	'''
	return datetime.datetime(1,1,1) + datetime.timedelta(microseconds=ticks//10)

def pandas_datatype_to_tabular_datatype(df:pd.DataFrame)-> Dict:
	'''WiP takes dataframe columns and gets respective tabular column datatype.
	<br/>([NumPy Datatypes](https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html) and [Tabular Datatypes](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.datatype?view=analysisservices-dotnet))

	Args:
		df (pd.DataFrame): Pandas DataFrame

	Returns:
		Dict: EX {'col1': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9700>, 'col2': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC8840>, 'col3': <Microsoft.AnalysisServices.Tabular.DataType object at 0x0000023BFFBC9800>}
	'''
	logging.info(f'Getting DF Column Dtypes to Tabular Dtypes...')
	tabular_datatype_mapping_key = {
		'b':DataType.Boolean,
		'i':DataType.Int64,
		'u':DataType.Int64,
		'f':DataType.Double,
		'c':DataType.Double,
		'm':DataType.DateTime,
		'M':DataType.DateTime,
		'O':DataType.String,
		'S':DataType.String,
		'U':DataType.String,
		'V':DataType.String
	}
	return {column:tabular_datatype_mapping_key[df[column].dtype.kind] for column in df.columns}

def pd_dataframe_to_dax_expression(df:pd.DataFrame = pd.DataFrame(data={'col1': [1.0, 2.0], 'col2': [3, 4]})) -> str:
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
	def dax_tableconstructor_rows_expression_generator(list_of_strings: list[str]) -> str:
		'''
		Converts list[str] to dax table rows for example ['one','two'] -> '('one','two')'
		'''
		return
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