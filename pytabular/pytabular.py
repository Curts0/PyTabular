
from typing import List, Tuple
from types import FunctionType
from collections import namedtuple
import clr
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular.json')
clr.AddReference('Microsoft.AnalysisServices')
from InquirerPy.base.control import Choice
from InquirerPy import inquirer, get_style
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection
from Microsoft.AnalysisServices.Tabular import Server, Database, RefreshType, ConnectionDetails, ColumnType
from Microsoft.AnalysisServices import UpdateOptions
import pandas as pd
def iterator(collection) -> List[Tuple]:
	'''
	Input a collection from Microsoft.Analysis.Services.Tabular.
	It will iterate through the C# collection and return a List[Tuple]
	Ex. [(Index,Collection Item, Name of Item)]
	'''
	return [(index, collection.get_Item(index).Name,collection.get_Item(index)) for index in range(len(collection))]

def find(iterator_collection: List[Tuple],names) -> List:
	'''
	Input should be the returned value from the iterator func
	and the specific name or names (in iterable format) to filter the list down
	'''
	if type(names) == str:
		names = [names]
	return [iterator_collection[key][0] for key,value in enumerate(iterator_collection) if iterator_collection[key][1] in names]


class Tabular:
	'''
	Tabular Class
	'''
	def __init__(self,CONNECTION_STR):
		self.Server = Server()
		self.Server.Connect(CONNECTION_STR)
		self.Catalog = self.Server.ConnectionInfo.Catalog
		self.Database = self.Server.Databases[find(iterator(self.Server.Databases),self.Catalog)[-1]]
		self.Model = self.Database.Model
		self.DaxConnection = AdomdConnection()
		self.DaxConnection.ConnectionString = f"{self.Server.ConnectionString}Password='{self.Server.ConnectionInfo.Password}'"
		self.Tables = iterator(self.Model.Tables)
		self.Columns = [iterator(table[2].Columns) for table in self.Tables]
		pass
	def Refresh(self, Collections, RefreshType=RefreshType.Full) -> None:
		'''
		Input iterable Collections for the function to run through.
		It will add the collection items into a Refresh Request.
		To execute refresh run through Update()
		'''
		for collection in Collections:
			collection.RequestRefresh(RefreshType)
	def Update(self, UpdateOptions=UpdateOptions.ExpandFull) -> None:
		'''
		Takes currently changed options in model then updates.
		'''
		return self.Database.Update(UpdateOptions)
	def Query(self,Query_Str) -> pd.DataFrame:
		'''
		Executes Query on Model and Returns Results in Pandas DataFrame
		'''
		try:
			self.DaxConnection.Open()
		except: 
			pass
		Query =  AdomdCommand(Query_Str, self.DaxConnection).ExecuteReader()
		Column_Headers = [(index,Query.GetName(index)) for index in range(0,Query.FieldCount)]
		Results = list()
		while Query.Read():
			Results.append([Query.GetValue(index) for index in range(0,len(Column_Headers))])
		Query.Close()
		df = pd.DataFrame(Results,columns=[value for _,value in Column_Headers])
		return df
	def Query_Every_Column(self,query_function='COUNTROWS(VALUES(_))') -> pd.DataFrame():
		'''
		Dynamically pull all tables and columns
		and perform a dax query to retrieve all counts
		outputs a dataframe
		'''
		query_str = "EVALUATE UNION(\n"
		for table in self.Columns:
			for column in table:
				if column[2].Type != ColumnType.RowNumber:
					table_name = column[2].Table.get_Name()
					column_name = column[2].get_Name()
					dax_identifier = f"'{table_name}'[{column_name}]"
					query_str += f"ROW(\"Table\",\"{table_name}\",\"Column\",\"{column_name}\",\"{query_function}\",{query_function.replace('_',dax_identifier)}),\n"
		query_str = f'{query_str[:-2]})'
		return self.Query(query_str)
'''
def cli():
	server_str = inquirer.select(
		message = "What do you want to access?:",
		choices = [server for server in CONNECTION_STR.keys()],
		style=style,
		default = None).execute()
	server = Server()
	server.Connect(CONNECTION_STR[server_str])

	databases = [server.Databases[x].get_Name() for x in range(0, len(server.Databases))]
	database_index = inquirer.select(
		message="Which DB do you want to access?",
		choices=[Choice(key, name=db_name) for key, db_name in enumerate(databases)],
		style=style
		).execute()
	database = server.Databases[database_index]
	command = inquirer.select(
		message = f"What do you want to do? You are currently connected to {databases[database_index]} in {server_str}",
		choices = ["Refresh Table","Refresh Partitions","Check Memory"],
		style= style
	).execute()
	tables = [(table_index,database.Model.Tables.get_Item(table_index).get_Name()) for table_index in range(0,database.Model.Tables.Count)]
	select_tables = inquirer.text(
		message =f"What table do you want to refresh?",
		completer = {database.Model.Tables.get_Item(table_index).get_Name():None for table_index in range(0,database.Model.Tables.Count)},
		style=style
	)
	match command:
		case "Refresh Table":
			table_to_refresh = select_tables.execute()
			table_index_to_refresh = [item[0] for item in tables if item[1] == table_to_refresh]

			for index in table_index_to_refresh:
				database.Model.Tables.get_Item(index).RequestRefresh(RefreshType.Full)

			confirm_refresh = inquirer.confirm(
				message=f"Execute Refresh Now?"
			).execute()
			if confirm_refresh:
				database.Update(UpdateOptions.ExpandFull)
			return True
		case "Refresh Partitions":
			select_tables._message = "From what table do you want to refresh partitions?"
			table = select_tables.execute()
			table_index_to_refresh = [item[0] for item in tables if item[1] == table]


		case "Check Memory":
			print(database.get_EstimatedSize())
	return database


if __name__ == '__main__':
	cli()
'''