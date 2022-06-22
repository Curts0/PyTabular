import clr
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices')
from InquirerPy.separator import Separator
from InquirerPy.base.control import Choice
from InquirerPy import inquirer
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand, AdomdConnection
from Microsoft.AnalysisServices.Tabular import Server, Database, RefreshType
from Microsoft.AnalysisServices import UpdateOptions





CONNECTION_STR = {"FIN 300": "Data Source=asazure://centralus.asazure.windows.net/azraasdaientdlfn300:rw;Initial Catalog=FINANCE;Cube=Model;User ID=svc-azssas-process-p@rockwellautomation.com;Password=');!3xk3YlB(Fatf'",
                  "FIN 500": "Data Source=asazure://centralus.asazure.windows.net/azraasdaientdlfn500:rw;Initial Catalog=FINANCE;Cube=Model;User ID=svc-azssas-process-p@rockwellautomation.com;Password=');!3xk3YlB(Fatf'",
                  "FIN 700": "Data Source=asazure://centralus.asazure.windows.net/azraasdaientdlfn700:rw;Initial Catalog=FINANCE;Cube=Model;User ID=svc-azssas-process-p@rockwellautomation.com;Password=');!3xk3YlB(Fatf'"}




class Tabular:
	def __init__(self,CONNECTION_STR=CONNECTION_STR['FIN 500']):
		self.Server = Server()
		self.Server.Connect(CONNECTION_STR)
		self.Database = 1
		self.Model = 1
		pass
	def pick_db(self,db_name='FINANCE'):
		databases = [(x, self.Server.Databases[x].get_Name()) for x in range(0, len(self.Server.Databases))]
		#db = self.Server.Databases[database_index]
		return databases




def main():

	server_str = inquirer.select(
		message = "What do you want to access?:",
		choices = [server for server in CONNECTION_STR.keys()],
		default = None).execute()
	server = Server()
	server.Connect(CONNECTION_STR[server_str])
	server.SessionTrace.Start()
	print(server.SessionTrace.IsStarted)

	databases = [server.Databases[x].get_Name() for x in range(0, len(server.Databases))]
	database_index = inquirer.select(
		message="Which DB do you want to access?",
		choices=[Choice(key, name=db_name) for key, db_name in enumerate(databases)]
		).execute()
	database = server.Databases[database_index]
	
	command = inquirer.select(
		message = f"What do you want to do? You are currently connected to {databases[database_index]} in {server_str}",
		choices = ["Refresh Table","Check Memory"]
	).execute()
	tables = [(table_index,database.Model.Tables.get_Item(table_index).get_Name()) for table_index in range(0,database.Model.Tables.Count)]
	select_tables = inquirer.text(
		message =f"What tables do you want to refresh?",
		completer = {database.Model.Tables.get_Item(table_index).get_Name():None for table_index in range(0,database.Model.Tables.Count)}
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

		case "Check Memory":
			print(database.get_EstimatedSize())
	server.SessionTrace.Stop()
	return database



# Request a Refresh - t.core.Databases[0].Model.Tables.get_Item(6).RequestRefresh(t.RefreshType.Full)
# Run a Refresh - t.core.Databases[0].Update(t.UpdateOptions.ExpandFull)
# Sync the latest data - t.core.Databases[0].Model.Sync()
#core = Server()
#core.Connect(CONNECTION_STR["FIN 500"])
#print(core.Name)

# query
'''
conn = AdomdConnection()
conn.ConnectionString = CONNECTION_STR["FIN 300"]
conn.Open()
query = AdomdCommand('EVALUATE TOPN(1000,FACT_COPA)', conn).ExecuteReader()
'''
# def read_all(query):
# while query.Read()
# .Read() will start at the first row and keep returning true if it finds data
