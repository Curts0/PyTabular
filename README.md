
# PyTabular
[![PyPI version](https://badge.fury.io/py/python-tabular.svg)](https://badge.fury.io/py/python-tabular)
[![Downloads](https://pepy.tech/badge/python-tabular)](https://pepy.tech/project/python-tabular)
[![readthedocs](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml)
[![pages-build-deployment](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment)

### What is it?

PyTabular (python-tabular in [pypi](https://pypi.org/project/python-tabular/)) is a python package that allows for programmatic execution on your tabular models! This is possible thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). The package should have the dll files included when you import it. See [Documentation Here](https://curts0.github.io/PyTabular/). PyTabular is still considered alpha while I'm working on building out the proper tests and testing environments, so I can ensure some kind of stability in features. Please send bugs my way! Preferably in the issues section in Github. I want to harden this project so many can use it easily. I currently have local pytest for python 3.6 to 3.11 and run those tests through a local AAS and Gen2 model.

### Getting Started
See the [Pypi project](https://pypi.org/project/python-tabular/) for available version.
```powershell
python3 -m pip install python-tabular
```

In your python environment, import pytabular and call the main Tabular Class. Only parameter needed is a solid connection string.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
```

You can query your models with the Query method from your tabular class. For Dax Queries, it will need the full Dax syntax. See [EVALUATE example](https://dax.guide/st/evaluate/). This will return a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html). If you are looking to return a single value, see below. Simply wrap your query in the the curly brackets. The method will take that single cell table and just return the individual value. You can also query your DMV. See below for example. See [PyTabular Docs for Query](https://curts0.github.io/PyTabular/Tabular/#query).
```python
#Run basic queries
DAX_QUERY = "EVALUATE TOPN(100, 'Table1')"
model.Query(DAX_QUERY) #returns pd.DataFrame()

#or...
DMV_QUERY = "select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"
model.Query(DMV_QUERY) #returns pd.DataFrame()

#or...
SINGLE_VALUE_QUERY_EX = "EVALUATE {1}"
model.Query(SINGLE_VALUE_QUERY_EX) #returns 1
```

Refresh method to handle refreshes on your model. This is synchronous. Should be flexible enough to handle a variety of inputs. See [PyTabular Docs for Refreshing Tables and Partitions](https://curts0.github.io/PyTabular/Tabular/#refresh). Most basic way to refresh is input the table name string. The method will search for table and output exeption if unable to find it. For partitions you will need a key, value combination. Example, {'Table1':'Partition1'}. You can also take the key value pair and iterate through a group of partitions. Example, {'Table1':['Partition1','Partition2']}. Rather than providing a string, you can also input the actual class. See below for those examples, and you can acess them from the built in attributes self.Tables, self.Partitions or explore through the .Net classes yourself in self.Model.Tables.
```python
#You have a few options when refreshing. 
model.Refresh('Table Name')

#or...
model.Refresh(['Table1','Table2','Table3'])

#or...
model.Refresh(<Table Class>)

#or...
model.Refresh(<Partition Class>)

#or...
model.Refresh({'Table Name':'Partition Name'})

#or any kind of weird combination like
model.Refresh([{<Table Class>:<Partition Class>,'Table Name':['Partition1','Partition2']},'Table Name','Table Name2'])

#Add Tracing=True for simple Traces tracking the refresh.
model.Refresh(['Table1','Table2'], Tracing=True)
```

### Use Cases

##### If blank table, then refresh table.
This will use the function [Return_Zero_Row_Tables](https://curts0.github.io/PyTabular/Examples/#return_zero_row_tables) and the method [Refresh](https://curts0.github.io/PyTabular/Tabular/#refresh) from the Tabular class.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
tables = pytabular.Return_Zero_Row_Tables()
if len(tables) > 0:
    model.Refresh(tables, Tracing = True) #Add a trace in there for some fun.
```

##### Sneak in a refresh.
This will use the method [Is_Process](https://curts0.github.io/PyTabular/Tabular/#is_process) and the method [Refresh](https://curts0.github.io/PyTabular/Tabular/#refresh) from the Tabular class. It will check the DMV to see if any jobs are currently running classified as processing.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
if model.Is_Process():
    #do what you want if there is a refresh happening
else:
    model.Refresh(TABLES_OR_PARTITIONS_TO_REFRESH)
```

##### Show refresh times in model.
This will use the function [Table_Last_Refresh_Times](https://curts0.github.io/PyTabular/Examples/#table_last_refresh_times) and the method [Create_Table](https://curts0.github.io/PyTabular/Tabular/#create_table) from the Tabular class. It will search through the model for all tables and partitions and pull the 'RefreshedTime' property from it. It will return results into a pandas dataframe, which will then be converted into an M expression used for a new table.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
df = pytabular.Table_Last_Refresh_Times(model, group_partition = False)
model.Create_Table(df, 'Refresh Times')
```


##### If BPA Violation, then revert deployment.
Uses a few things. First the [BPA Class](https://curts0.github.io/PyTabular/Best%20Practice%20Analyzer/#bpa), then the [TE2 Class](https://curts0.github.io/PyTabular/Tabular%20Editor%202/), and will finish with the [Analyze_BPA](https://curts0.github.io/PyTabular/Tabular/#analyze_bpa) method. Did not want to re-invent the wheel with the amazing work done with Tabular Editor and it's BPA capabilities.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
TE2 = pytabular.TE2() #Feel free to input your TE2 File path or this will download for you.
BPA = pytabular.BPA() #Fee free to input your own BPA file or this will download for you from: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
results = model.Analyze_BPA(TE2.EXE,BPA.Location)

if len(results) > 0:
    #Revert deployment here!
```

##### Backup & Revert a Table.
USE WITH CAUTION, obviously not in PROD. I have been experimenting with this concept. Made for selfish reasons. Will probably get removed and I'll keep in my own local version. But fun to work with. Uses two methods. [Backup_Table](https://curts0.github.io/PyTabular/Tabular/#backup_table) and [Revert_Table](https://curts0.github.io/PyTabular/Tabular/#revert_table)

```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
model.Backup_Table('TableName') #This will backup the table with surround items (columns,measures,relationships,roles,hierarchies,etc.) and will add a suffix of '_backup'
#-----------#
#Make any changes to your original table and then revert or delete backup as necessary
#-----------#
model.Revert_Table('TableName') #This will essentially replace your original with _backup
```