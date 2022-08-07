import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
import clr
logging.debug('Adding Reference Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
logging.debug('Adding Reference Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
logging.debug('Adding Reference Microsoft.AnalysisServices')
clr.AddReference('Microsoft.AnalysisServices')
logging.debug(f'Importing Microsoft.AnalysisServices.AdomdClient')
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection
logging.debug(f'Importing Microsoft.AnalysisServices.Tabular')
from Microsoft.AnalysisServices.Tabular import Server, Database, RefreshType, DataType, ConnectionDetails, ColumnType, MetadataPermission, Table, DataColumn, Partition, MPartitionSource, PartitionSourceType
logging.debug(f'Importing Microsoft.AnalysisServices')
from Microsoft.AnalysisServices import UpdateOptions

logging.debug('Importing Other Packages...')
from typing import List
import requests as r
import pandas as pd
import json
import os
import subprocess
import atexit
from logic_utils import pd_dataframe_to_m_expression, pandas_datatype_to_tabular_datatype

class Tabular:
	'''Input Connection String then you are off to the races...
		This will be your best friend: [Microsoft.AnalysisServices.Tabular](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet)

	Args:
		CONNECTION_STR (str): (https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions)
	'''	
	def __init__(self,CONNECTION_STR:str):
		logging.debug(f'Initializing Tabular Class')
		self.Server = Server()
		self.Server.Connect(CONNECTION_STR)
		logging.debug(f'Connected to Server - {self.Server.Name}')
		self.Catalog = self.Server.ConnectionInfo.Catalog
		self.Database = self.Server.Databases.Find(self.Catalog)
		logging.debug(f'Connected to Database - {self.Database.Name}')
		self.Model = self.Database.Model
		logging.debug(f'Connected to Model - {self.Model.Name}')
		self.DaxConnection = AdomdConnection()
		self.DaxConnection.ConnectionString = f"{self.Server.ConnectionString}Password='{self.Server.ConnectionInfo.Password}'"
		self.Tables = [table for table in self.Model.Tables.GetEnumerator()]
		self.Columns = [column for table in self.Tables for column in table.Columns.GetEnumerator()]
		self.Partitions = [partition for table in self.Tables for partition in table.Partitions.GetEnumerator()]
		self.Measures = [measure for table in self.Tables for measure in table.Measures.GetEnumerator()]
		logging.debug(f'Class Initialization Completed')
		logging.debug(f'Registering Disconnect on Termination...')
		atexit.register(self.Disconnect)
		pass
	def __repr__(self) -> str:
		return f'{self.Server.Name}::{self.Database.Name}::{self.Model.Name}\n{self.Database.EstimatedSize} Estimated Size\n{len(self.Tables)} Tables\n{len(self.Columns)} Columns\n{len(self.Partitions)} Partitions\n{len(self.Measures)} Measures'
	def Disconnect(self) -> bool:
		'''Disconnects from Model

		Returns:
			bool: True if successful
		'''
		logging.debug(f'Disconnecting from - {self.Server.Name}')
		self.Server.Disconnect()
		
		if self.Server.Connected:
			logging.error(f'Disconnect Unsuccessful')
			return False
		else:
			logging.debug(f'Disconnect Successful')
			return True	
	def Refresh(self, iterable_items: List, RefreshType=RefreshType.Full) -> None:
		'''Input iterable Collections for the function to run through.
		It will add the collection items into a Refresh Request.
		To execute refresh run through Update()

		Args:
			iterable_items (List): Must be refreshable Tabular objects.
			RefreshType (_type_, optional): _description_. Defaults to RefreshType.Full.
		'''	
		for collection in iterable_items:
			logging.debug(f'Adding {collection.Name} to Refresh Request')
			collection.RequestRefresh(RefreshType)
	def Update(self, UpdateOptions:UpdateOptions =UpdateOptions.ExpandFull) -> None:
		'''Really just this... https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.majorobject.update?view=analysisservices-dotnet#microsoft-analysisservices-majorobject-update(microsoft-analysisservices-updateoptions)

		Args:
			UpdateOptions (UpdateOptions, optional): See above MS Doc link. Defaults to UpdateOptions.ExpandFull.

		Returns:
			None: Placeholder to eventually change.
		'''
		logging.debug('Running Update Request')
		return self.Database.Update(UpdateOptions)
	def Backup_Table(self,table_str:str) -> bool:
		'''USE WITH CAUTION, EXPERIMENTAL. Backs up table in memory, brings with it measures, columns, hierarchies, relationships, roles, etc.
		It will add suffix '_backup' to all objects.
		Refresh is performed from source during backup.

		Args:
			table_str (str, optional): Name of Table.

		Returns:
			bool: Returns True if Successful, else will return error.
		'''		
		logging.info('Backup Beginning...')
		logging.debug(f'Cloning {table_str}')
		table = self.Model.Tables.Find(table_str).Clone()
		logging.info(f'Beginning Renames')
		def rename(items):
			for item in items:
				item.RequestRename(f'{item.Name}_backup')
				logging.debug(f'Renamed - {item.Name}')
		logging.info('Renaming Columns')
		rename(table.Columns.GetEnumerator())
		logging.info('Renaming Partitions')
		rename(table.Partitions.GetEnumerator())
		logging.info('Renaming Measures')
		rename(table.Measures.GetEnumerator())
		logging.info('Renaming Hierarchies')
		rename(table.Hierarchies.GetEnumerator())
		logging.info('Renaming Table')
		table.RequestRename(f'{table.Name}_backup')
		logging.info('Adding Table to Model as backup')
		self.Model.Tables.Add(table)
		logging.info('Finding Necessary Relationships... Cloning...')
		relationships = [relationship.Clone() for relationship in self.Model.Relationships.GetEnumerator() if relationship.ToTable.Name == table.Name.removesuffix('_backup') or relationship.FromTable.Name == table.Name.removesuffix('_backup')]
		logging.info('Renaming Relationships')
		rename(relationships)
		logging.info('Switching Relationships to Clone Table & Column')
		for relationship in relationships:
			logging.debug(f'Renaming - {relationship.Name}')
			if relationship.ToTable.Name == table.Name.removesuffix('_backup'):
				relationship.set_ToColumn(table.Columns.Find(f'{relationship.ToColumn.Name}_backup'))
			elif relationship.FromTable.Name == table.Name.removesuffix('_backup'):
				relationship.set_FromColumn(table.Columns.Find(f'{relationship.FromColumn.Name}_backup'))
			logging.debug(f'Adding {relationship.Name} to {self.Model.Name}')
			self.Model.Relationships.Add(relationship)
		def clone_role_permissions():
			logging.info(f'Beginning to handle roles and permissions for table...')
			logging.debug(f'Finding Roles...')
			roles = [role for role in self.Model.Roles.GetEnumerator() for tablepermission in role.TablePermissions.GetEnumerator() if tablepermission.Name == table_str]
			for role in roles:
				logging.debug(f'Role {role.Name} matched, looking into it...')
				logging.debug(f'Searching for table specific permissions')
				tablepermissions = [table.Clone() for table in role.TablePermissions.GetEnumerator() if table.Name == table_str]
				for tablepermission in tablepermissions:
					logging.debug(f'{tablepermission.Name} found... switching table to clone')
					tablepermission.set_Table(table)
					for column in tablepermission.ColumnPermissions.GetEnumerator():
						logging.debug(f'Column - {column.Name} copying permissions to clone...')
						column.set_Column(self.Model.Tables.Find(table.Name).Columns.Find(f'{column.Name}_backup'))
					logging.debug(f'Adding {tablepermission.Name} to {role.Name}')
					role.TablePermissions.Add(tablepermission)
			return True
		clone_role_permissions()
		logging.info(f'Refreshing Clone... {table.Name}')
		self.Refresh([table])
		logging.info(f'Updating Model {self.Model.Name}')
		self.Update()
		return True
	def Revert_Table(self, table_str:str) -> bool:
		'''USE WITH CAUTION, EXPERIMENTAL. This is used in conjunction with Backup_Table().
		It will take the 'TableName_backup' and replace with the original.
		Example scenario -> 
		1. model.Backup_Table('TableName')
		2. #perform any proposed changes in original 'TableName'
		3. #validate changes in 'TableName'
		4. #if unsuccessful run model.Revert_Table('TableName')

		Args:
			table_str (str): Name of table.

		Returns:
			bool: Returns True if Successful, else will return error.
		'''		
		'''

		'''
		logging.info(f'Beginning Revert for {table_str}')
		logging.debug(f'Finding original {table_str}')
		main = self.Model.Tables.Find(table_str)
		logging.debug(f'Finding backup {table_str}')
		backup = self.Model.Tables.Find(f'{table_str}_backup')
		logging.debug(f'Finding original relationships')
		main_relationships = [relationship for relationship in self.Model.Relationships.GetEnumerator() if relationship.ToTable.Name == main.Name or relationship.FromTable.Name == main.Name]
		logging.debug(f'Finding backup relationships')
		backup_relationships = [relationship for relationship in self.Model.Relationships.GetEnumerator() if relationship.ToTable.Name == backup.Name or relationship.FromTable.Name == backup.Name]
		
		def remove_role_permissions():
			logging.debug(f'Finding table and column permission in roles to remove from {table_str}')
			roles = [role for role in self.Model.Roles.GetEnumerator() for tablepermission in role.TablePermissions.GetEnumerator() if tablepermission.Name == table_str]
			for role in roles:
				logging.debug(f'Role {role.Name} Found')
				tablepermissions = [table for table in role.TablePermissions.GetEnumerator() if table.Name == table_str]
				for tablepermission in tablepermissions:
					logging.debug(f'Removing {tablepermission.Name} from {role.Name}')
					role.TablePermissions.Remove(tablepermission)
		for relationship in main_relationships:
			logging.debug(f'Cleaning relationships...')
			if relationship.ToTable.Name == main.Name:
				logging.debug(f'Removing {relationship.Name}')
				self.Model.Relationships.Remove(relationship)
			elif relationship.FromTable.Name == main.Name:
				logging.debug(f'Removing {relationship.Name}')
				self.Model.Relationships.Remove(relationship)
		logging.debug(f'Removing Original Table {main.Name}')
		self.Model.Tables.Remove(main)
		remove_role_permissions()
		def dename(items):
			for item in items:
				logging.debug(f'Removing Suffix for {item.Name}')
				item.RequestRename(f'{item.Name}'.removesuffix('_backup'))
				logging.debug(f'Saving Changes... for {item.Name}')
				self.Model.SaveChanges()
		logging.info(f'Name changes for Columns...')
		dename([column for column in backup.Columns.GetEnumerator() if column.Type != ColumnType.RowNumber])
		logging.info(f'Name changes for Partitions...')
		dename(backup.Partitions.GetEnumerator())
		logging.info(f'Name changes for Measures...')
		dename(backup.Measures.GetEnumerator())
		logging.info(f'Name changes for Hierarchies...')
		dename(backup.Hierarchies.GetEnumerator())
		logging.info(f'Name changes for Relationships...')
		dename(backup_relationships)
		logging.info(f'Name changes for Backup Table...')
		backup.RequestRename(backup.Name.removesuffix('_backup'))
		self.Update()
		return True
	def Query(self,Query_Str:str) -> pd.DataFrame:
		'''	Executes Query on Model and Returns Results in Pandas DataFrame

		Args:
			Query_Str (str): Dax Query. Note, needs full syntax (ex: EVALUATE). See https://docs.microsoft.com/en-us/dax/dax-queries 

		Returns:
			pd.DataFrame: Returns dataframe with results
		'''
		logging.info(f'Query Called...')
		try:
			logging.debug(f'Attempting to Open Connection...')
			self.DaxConnection.Open()
			logging.debug(f'Connected!')
		except: 
			logging.debug(f'Connection skipped already connected...')
			pass
		logging.debug(f'Querying Model with Query...')
		Query =  AdomdCommand(Query_Str, self.DaxConnection).ExecuteReader()
		logging.debug(f'Determining Field Count...')
		Column_Headers = [(index,Query.GetName(index)) for index in range(0,Query.FieldCount)]
		Results = list()
		logging.debug(f'Converting Results into List...')
		while Query.Read():
			Results.append([Query.GetValue(index) for index in range(0,len(Column_Headers))])
		logging.debug(f'Data retrieved and closing query...')
		Query.Close()
		logging.debug(f'Converting to Pandas DataFrame...')
		df = pd.DataFrame(Results,columns=[value for _,value in Column_Headers])
		return df
	def Query_Every_Column(self,query_function:str='COUNTROWS(VALUES(_))') -> pd.DataFrame:
		'''This will dynamically create a query to pull all columns from the model and run the query function.
		It will replace the _ with the column to run.

		Args:
			query_function (str, optional): Dax query is dynamically building a query with the UNION & ROW DAX Functions.
			Example -> 
			EVALUATE
			UNION(
				ROW("Table_Name", "Table1", "Column_Name", "Column1", "COUNTROWS(VALUES(_))", COUNTROWS(VALUES("Column1"))),
				ROW("Table_Name", "Table1", "Column_Name", "Column2", "COUNTROWS(VALUES(_))", COUNTROWS(VALUES("Column2"))),
				ROW("Table_Name", "Table2", "Column_Name", "Column1", "COUNTROWS(VALUES(_))", COUNTROWS(VALUES("Column1")))
			)

			Defaults to 'COUNTROWS(VALUES(_))'.

		Returns:
			pd.DataFrame: Returns dataframe with results.
		'''
		logging.info(f'Beginning execution of querying every column...')
		logging.debug(f'Function to be run: {query_function}')
		logging.debug(f'Dynamically creating DAX query...')
		query_str = "EVALUATE UNION(\n"
		for column in self.Columns:
			if column.Type != ColumnType.RowNumber:
				table_name = column.Table.get_Name()
				column_name = column.get_Name()
				dax_identifier = f"'{table_name}'[{column_name}]"
				query_str += f"ROW(\"Table\",\"{table_name}\",\"Column\",\"{column_name}\",\"{query_function}\",{query_function.replace('_',dax_identifier)}),\n"
		query_str = f'{query_str[:-2]})'
		return self.Query(query_str)
	def Query_Every_Table(self,query_function:str='COUNTROWS(_)') -> pd.DataFrame:
		'''This will dynamically create a query to pull all tables from the model and run the query function.
		It will replace the _ with the table to run.

		Args:
			query_function (str, optional): Dax query is dynamically building a query with the UNION & ROW DAX Functions.
			Example -> 
			EVALUATE
			UNION(
				ROW("Table_Name", "Table1", "COUNTROWS(_)", COUNTROWS("Table1")),
				ROW("Table_Name", "Table2", "COUNTROWS(_)", COUNTROWS("Table2")),
				ROW("Table_Name", "Table3", "COUNTROWS(_)", COUNTROWS("Table3"))
			). Defaults to 'COUNTROWS(_)'.

		Returns:
			pd.DataFrame: Returns dataframe with results
		'''
		logging.info(f'Beginning execution of querying every table...')
		logging.debug(f'Function to be run: {query_function}')
		logging.debug(f'Dynamically creating DAX query...')
		query_str = "EVALUATE UNION(\n"
		for table in self.Tables:
			table_name = table.get_Name()
			dax_table_identifier = f'\'{table_name}\''
			query_str += f"ROW(\"Table\",\"{table_name}\",\"{query_function}\",{query_function.replace('_',dax_table_identifier)}),\n"
		query_str = f'{query_str[:-2]})'
		return self.Query(query_str)
	def Analyze_BPA(self,Tabular_Editor_Exe:str,Best_Practice_Analyzer:str) -> List[str]:
		'''Takes your Tabular Model and performs TE2s BPA. Runs through Command line.
		https://docs.tabulareditor.com/te2/Best-Practice-Analyzer.html
		https://docs.tabulareditor.com/te2/Command-line-Options.html

		Args:
			Tabular_Editor_Exe (str): TE2 Exe File path. Feel free to use class TE2().EXE_Path or provide your own.
			Best_Practice_Analyzer (str): BPA json file path. Feel free to use class BPA().Location or provide your own. Defualts to 	https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json

		Returns:
			List[str]: Assuming no failure, will return list of BPA violations. Else will return error from command line.
		'''		
		#Working TE2 Script in Python os.system(f"start /wait {te2.EXE_Path} \"Provider=MSOLAP;{model.DaxConnection.ConnectionString}\" FINANCE -B \"{os.getcwd()}\\Model.bim\" -A {l.BPA_LOCAL_FILE_PATH} -V/?")
		#start /wait 
		logging.debug(f'Beginning request to talk with TE2 & Find BPA...')
		cmd = f"{Tabular_Editor_Exe} \"Provider=MSOLAP;{self.DaxConnection.ConnectionString}\" {self.Database.Name} -B \"{os.getcwd()}\\Model.bim\" -A {Best_Practice_Analyzer} -V/?"
		logging.debug(f'Command Generated')
		logging.debug(f'Submitting Command...')
		sp = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
		raw_output,error = sp.communicate()
		if len(error) > 0:
			return error
		else:
			return [output for output in raw_output.split('\n') if 'violates rule' in output]
	def Create_Table(self,df:pd.DataFrame, table_name:str) -> bool:
		'''Creates tables from pd.DataFrame as an M-Partition. 
		So will convert the dataframe to M-Partition logic via the M query table constructor.
		Runs refresh and will update model.

		Args:
			df (pd.DataFrame): DataFrame to add to model
			table_name (str): _description_

		Returns:
			bool: True if successful
		'''	
		logging.debug(f'Beginning to create table for {table_name}...')
		new_table = Table()
		new_table.RequestRename(table_name)
		logging.debug(f'Sorting through columns...')
		df_column_names = df.columns
		dtype_conversion = pandas_datatype_to_tabular_datatype(df)
		for df_column_name in df_column_names:
			logging.debug(f'Adding {df_column_name} to Table...')
			column = DataColumn()
			column.RequestRename(df_column_name)
			column.set_SourceColumn(df_column_name)
			column.set_DataType(dtype_conversion[df_column_name])
			new_table.Columns.Add(column)
		logging.debug(f'Expression String Created...')
		logging.debug(f'Creating MPartition...')
		partition = Partition()
		partition.set_Source(MPartitionSource())
		logging.debug(f'Setting MPartition Expression...')
		partition.Source.set_Expression(pd_dataframe_to_m_expression(df))
		logging.debug(f'Adding partition: {partition.Name} to {self.Server.Name}::{self.Database.Name}::{self.Model.Name}')
		new_table.Partitions.Add(partition)
		logging.debug(f'Adding table: {new_table.Name} to {self.Server.Name}::{self.Database.Name}::{self.Model.Name}')
		self.Model.Tables.Add(new_table)
		self.Refresh([new_table])
		self.Update()
		return True



class BPA:
	'''
	Best Practice Analyzer Class 
	Can provide Url, Json File Path, or Python List.
	If nothing is provided it will default to Microsofts Analysis Services report with BPA Rules.
	https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
	'''
	def __init__(self,rules_location:str='https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json') -> None:
		'''
		'''
		self.Location = rules_location
		self.Rules:list[dict()] = []
		logging.debug(f'Initializing BPA Class with: {rules_location}')
		try:
			logging.debug(f'Searching for Rules on the good ol\' internet...')
			self.Rules = r.get(rules_location).json()
			logging.debug(f'Rules recieved from: {rules_location}')
		except:
			logging.debug(f'Request to {rules_location} failed...')
			logging.debug(f'Searching for Rules locally with file path...')
			with open(rules_location,'r') as json_file:
				self.Rules = json.load(json_file)
			logging.debug(f'Rules from file path collected...')
		pass
#Todo... subclass with a namedtuple
class TE2:
	'''
	TE2 Class, to use any built TabularEditor Command Line Scripts
	https://docs.tabulareditor.com/te2/Command-line-Options.html
	#https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip
	#https://cdn.tabulareditor.com/files/TabularEditor.2.16.7.zip
	'''
	def __init__(self,TE_Location='https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip') -> None:
		logging.debug(f'Checking for TE2 in {os.getcwd()}')
		te2_path = os.path.join(os.getcwd(),'TE2')
		if os.path.exists(te2_path) == False:
			logging.debug('Downloading Tabular Editor for BPA...')
			self.TE_Location = TE_Location
			response = r.get(self.TE_Location)
			file_location = f"{os.getcwd()}\\{self.TE_Location.split('/')[-1]}"
			with open(file_location,'wb') as te2:
				te2.write(response.content)
			logging.debug('TE2 Zip Download Complete!')
			logging.debug('Import ZipFile')
			import zipfile as Z
			logging.debug('Unzipping file...')
			with Z.ZipFile(file_location) as zip:
				zip.extractall(path=te2_path)
			logging.debug('All Unzipped!')
			logging.debug('Removing Zip File')
			os.remove(file_location)
		else:
			logging.debug(f'TE2 Directory Found with Files {os.listdir(path=te2_path)}')
		self.EXE_Path = os.path.join(te2_path,'TabularEditor.exe')
		if os.path.exists(self.EXE_Path):
			logging.debug(f'TabularEditor.exe Located! {self.EXE_Path}')
		else:
			logging.error('TabularEditor.exe not found!')
		pass
	pass
