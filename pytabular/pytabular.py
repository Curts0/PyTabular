
from typing import List, Tuple
from types import FunctionType
from collections import namedtuple, OrderedDict
import clr
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular.json')
clr.AddReference('Microsoft.AnalysisServices')
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection
from Microsoft.AnalysisServices.Tabular import Server, Database, RefreshType, ConnectionDetails, ColumnType, MetadataPermission
from Microsoft.AnalysisServices import UpdateOptions
import pandas as pd
import logging
import sys
'''
log = logging.getLogger('PyTabular')
logformat = logging.Formatter(fmt='%(name)s :: %(levelname)-8s :: %(message)s')
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter('%(ascitime)s :: %(levelname)-8s :: %(message)s')
consoleHandler.setLevel(logging.INFO)
log.addHandler(consoleHandler)
'''
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(levelname)-8s :: %(message)s')

class Tabular:
	'''
	Tabular Class
	'''
	def __init__(self,CONNECTION_STR):
		logging.debug(f'Initializing Tabular Class')
		self.Server = Server()
		self.Server.Connect(CONNECTION_STR)
		logging.debug(f'Connected to Server - {self.Server.Name}')
		self.Catalog = self.Server.ConnectionInfo.Catalog
		self.Database = self.Server.Databases.Find(self.Catalog)
		logging.debug(f'Connected to Database - {self.Database.Name}')
		self.Model = self.Database.Model
		self.DaxConnection = AdomdConnection()
		self.DaxConnection.ConnectionString = f"{self.Server.ConnectionString}Password='{self.Server.ConnectionInfo.Password}'"
		self.Tables = [table for table in self.Model.Tables.GetEnumerator()]
		self.Columns = [column for table in self.Tables for column in table.Columns.GetEnumerator()]
		self.Partitions = [partition for table in self.Tables for partition in table.Partitions.GetEnumerator()]
		self.Measures = [measure for table in self.Tables for measure in table.Measures.GetEnumerator()]
		logging.debug(f'Class Initialization Completed')
		pass
	def Disconnect(self) -> bool:
		'''
		Self explanatory. Runs self.Server.Disconnect()
		For logging purposes will check if disconnect successful.
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
		'''
		Input iterable Collections for the function to run through.
		It will add the collection items into a Refresh Request.
		To execute refresh run through Update()
		'''
		for collection in iterable_items:
			logging.debug(f'Adding {collection.Name} to Refresh Request')
			collection.RequestRefresh(RefreshType)
	def Update(self, UpdateOptions=UpdateOptions.ExpandFull) -> None:
		'''
		Takes currently changed options in model then updates.
		'''
		logging.debug('Running Update Request')
		return self.Database.Update(UpdateOptions)
	def Backup_Table(self,table_str:str = 'Table Name'):
		'''
		1. Clone Table
			Rename every column, partition, measure, hierarchy with suffix _backup
			Backup RLS & OLS for Table
				Scan through every Role
					If Role contains table, clone it
					set_Table to backup table
					set_Column to backup columns
					set_FilterExpressions to back references
					add to Role

		2. Refresh Clone Table 
		3. Find all relationship for that table
			Clone, rename with _backup and replace with column from clone table
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
	def Revert_Table(self, table_str:str = 'Table Name'):
		'''
		1. Remove main table
		2. Rename suffix in backup table
		3. Update
		'''
		main = self.Model.Tables.Find(table_str)
		backup = self.Model.Tables.Find(f'{table_str}_backup')
		main_relationships = [relationship for relationship in self.Model.Relationships.GetEnumerator() if relationship.ToTable.Name == main.Name or relationship.FromTable.Name == main.Name]
		backup_relationships = [relationship for relationship in self.Model.Relationships.GetEnumerator() if relationship.ToTable.Name == backup.Name or relationship.FromTable.Name == backup.Name]
		
		def remove_role_permissions():
			roles = [role for role in self.Model.Roles.GetEnumerator() for tablepermission in role.TablePermissions.GetEnumerator() if tablepermission.Name == table_str]
			for role in roles:
				tablepermissions = [table for table in role.TablePermissions.GetEnumerator() if table.Name == table_str]
				for tablepermission in tablepermissions:
					role.TablePermissions.Remove(tablepermission)
		for relationship in main_relationships:
			if relationship.ToTable.Name == main.Name:
				self.Model.Relationships.Remove(relationship)
			elif relationship.FromTable.Name == main.Name:
				self.Model.Relationships.Remove(relationship)
		self.Model.Tables.Remove(main)
		remove_role_permissions()
		def dename(items):
			for item in items:
				print(item.Name)
				item.RequestRename(f'{item.Name}'.removesuffix('_backup'))
				self.Model.SaveChanges()
		#[column for column in backup.Columns.GetEnumerator() if column.Type != ColumnType.RowNumber]
		dename([column for column in backup.Columns.GetEnumerator() if column.Type != ColumnType.RowNumber])
		dename(backup.Partitions.GetEnumerator())
		dename(backup.Measures.GetEnumerator())
		dename(backup.Hierarchies.GetEnumerator())
		dename(backup_relationships)
		backup.RequestRename(backup.Name.removesuffix('_backup'))
		self.Update()
		return True
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
		This will dynamically create a query to pull all columns from the model and run the query function.
		It will replace the _ with the column to run.
		'''
		query_str = "EVALUATE UNION(\n"
		for column in self.Columns:
			if column.Type != ColumnType.RowNumber:
				table_name = column.Table.get_Name()
				column_name = column.get_Name()
				dax_identifier = f"'{table_name}'[{column_name}]"
				query_str += f"ROW(\"Table\",\"{table_name}\",\"Column\",\"{column_name}\",\"{query_function}\",{query_function.replace('_',dax_identifier)}),\n"
		query_str = f'{query_str[:-2]})'
		return self.Query(query_str)
	def Query_Every_Table(self,query_function='COUNTROWS(_)') -> pd.DataFrame():
		'''
		This will dynamically create a query to pull all tables from the model and run the query function.
		It will replace the _ with the table to run.
		'''
		query_str = "EVALUATE UNION(\n"
		for table in self.Tables:
			table_name = table.get_Name()
			dax_table_identifier = f'\'{table_name}\''
			query_str += f"ROW(\"Table\",\"{table_name}\",\"{query_function}\",{query_function.replace('_',dax_table_identifier)}),\n"
		query_str = f'{query_str[:-2]})'
		return self.Query(query_str)