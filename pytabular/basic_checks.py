import logging
from typing import List
import pytabular
from logic_utils import ticks_to_datetime
import sys
import pandas as pd

def Return_Zero_Row_Tables(model:pytabular.Tabular) -> List[str]:
	'''	Returns list of table names of those that are returning isna()

	Args:
		model (pytabular.Tabular): Tabular Model

	Returns:
		List[str]: List of table names where DAX COUNTROWS('Table Name') is nan or 0.
	'''	
	logging.info(f'Executing Basic Function {sys._getframe(0).f_code.co_name}')
	query_function: str = 'COUNTROWS(_)'
	df: pd.DataFrame = model.Query_Every_Table(query_function)
	return df[df[f'[{query_function}]'].isna()]['[Table]'].to_list()

def Table_Last_Refresh_Times(model:pytabular.Tabular, group_partition:bool = True) -> pd.DataFrame:
	'''	Returns pd.DataFrame of tables with their latest refresh time. 
	Optional 'group_partition' variable, default is True.
	If False an extra column will be include to have the last refresh time to the grain of the partition
	Example to add to model model.Create_Table(p.Table_Last_Refresh_Times(model),'RefreshTimes')

	Args:
		model (pytabular.Tabular): Tabular Model
		group_partition (bool, optional): Whether or not you want the grain of the dataframe to be by table or by partition. Defaults to True.

	Returns:
		pd.DataFrame: pd dataframe with the RefreshedTime property: https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition.refreshedtime?view=analysisservices-dotnet#microsoft-analysisservices-tabular-partition-refreshedtime
		If group_partition == True and the table has multiple partitions, then df.groupby(by["tables"]).max()
	'''	
	logging.info(f'Executing Basic Function {sys._getframe(0).f_code.co_name}')
	data = {\
		"Tables":[partition.Table.Name for partition in model.Partitions],\
		"Partitions":[partition.Name for partition in model.Partitions],\
		"RefreshedTime":[ticks_to_datetime(partition.RefreshedTime.Ticks).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] for partition in model.Partitions]\
	}
	df = pd.DataFrame(data)
	if group_partition:
		logging.debug('Grouping together to grain of Table')
		return df[["Tables","RefreshedTime"]].groupby(by=["Tables"]).max().reset_index(drop=False)
	else:
		logging.debug('Returning DF')
		return df

def BPA_Violations_To_DF(model:pytabular.Tabular,te2:str, bpa:str) -> pd.DataFrame:
	results = model.Analyze_BPA(te2,bpa)
	data = [rule.replace(' violates rule ','^').replace('\"','').split('^') for rule in results]
	columns = ["Object","Violation"]
	return pd.DataFrame(data,columns=columns)