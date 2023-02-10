
# PyTabular
[![PyPI version](https://badge.fury.io/py/python-tabular.svg)](https://badge.fury.io/py/python-tabular)
[![Downloads](https://pepy.tech/badge/python-tabular)](https://pepy.tech/project/python-tabular)
[![readthedocs](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml)
[![pages-build-deployment](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment)
[![flake8](https://github.com/Curts0/PyTabular/actions/workflows/flake8.yml/badge.svg?branch=master)](https://github.com/Curts0/PyTabular/actions/workflows/flake8.yml)
[![docstr-coverage](https://github.com/Curts0/PyTabular/actions/workflows/docstr-coverage.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/docstr-coverage.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
### What is it?

[PyTabular](https://github.com/Curts0/PyTabular) (python-tabular in [pypi](https://pypi.org/project/python-tabular/)) is a python package that allows for programmatic execution on your tabular models! This is possible thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). Currently, this build is tested and working on Windows Operating System only. Help is needed to expand this for other operating systems. The package should have the dll files included when you import it. See [Documentation Here](https://curts0.github.io/PyTabular/). PyTabular is still considered alpha while I'm working on building out the proper tests and testing environments, so I can ensure some kind of stability in features. Please send bugs my way! Preferably in the issues section in Github. I want to harden this project so many can use it easily. I currently have local pytest for python 3.6 to 3.10 and run those tests through a local AAS and Gen2 model.

### Getting Started
See the [Pypi project](https://pypi.org/project/python-tabular/) for available versions. **To become PEP8 compliant with naming conventions, serious name changes were made in 0.3.5.** Instal v. 0.3.4 or lower to get the older naming conventions.
```powershell
python3 -m pip install python-tabular

#install specific version
python3 -m pip install python-tabular==0.3.4
```

In your python environment, import pytabular and call the main Tabular Class. Only parameter needed is a solid connection string.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
```

I'm a big fan of logging, if you don't want any just get the logger and disable it.
```python
import pytabular
pytabular.logger.disabled = True
```

You can query your models with the Query method from your tabular class. For Dax Queries, it will need the full Dax syntax. See [EVALUATE example](https://dax.guide/st/evaluate/). This will return a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html). If you are looking to return a single value, see below. Simply wrap your query in the the curly brackets. The method will take that single cell table and just return the individual value. You can also query your DMV. See below for example. See [PyTabular Docs for Query](https://curts0.github.io/PyTabular/Tabular/#query).
```python
#Run basic queries
DAX_QUERY = "EVALUATE TOPN(100, 'Table1')"
model.query(DAX_QUERY) #returns pd.DataFrame()

#or...
DMV_QUERY = "select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"
model.query(DMV_QUERY) #returns pd.DataFrame()

#or...
SINGLE_VALUE_QUERY_EX = "EVALUATE {1}"
model.query(SINGLE_VALUE_QUERY_EX) #returns 1

#or...
FILE_PATH = 'C:\\FILEPATHEXAMPLE\\file.dax' #or file.txt
model.query(FILE_PATH) #Will return same logic as above, single values if possible else will return pd.DataFrame()
```

You can also explore your tables, partitions, and columns. Via the Attributes from your Tabular class.
```python
#Explore tables...
dir(model.Tables['Table Name'])

#Explore columns & partitions
dir(model.Tables['Table Name'].Partitions['Partition Name'])

#Only a few features right now, but check out the built in methods.
model.Tables['Table Name'].refresh()
#or
model.Tables['Table Name'].Partitions['Partition Name'].refresh()
#or
model.Tables['Table Name'].Partitions['Partition Name'].last_refresh()
#or
model.Tables['Table Name'].row_count()
#or
model.Tables['Table Name'].Columns['Column Name'].distinct_count()
```

Refresh method to handle refreshes on your model. This is synchronous. Should be flexible enough to handle a variety of inputs. See [PyTabular Docs for Refreshing Tables and Partitions](https://curts0.github.io/PyTabular/Tabular/#refresh). Most basic way to refresh is input the table name string. The method will search for table and output exeption if unable to find it. For partitions you will need a key, value combination. Example, `{'Table1':'Partition1'}`. You can also take the key value pair and iterate through a group of partitions. Example, `{'Table1':['Partition1','Partition2']}`. Rather than providing a string, you can also input the actual class. See below for those examples, and you can acess them from the built in attributes `self.Tables`, `self.Partitions` or explore through the .Net classes yourself in `self.Model.Tables`.
```python
#You have a few options when refreshing. 
model.refresh('Table Name')

#or...
model.refresh(['Table1','Table2','Table3'])

#or...
model.refresh(<Table Class>)

#or...
model.refresh(<Partition Class>)

#or...
model.refresh({'Table Name':'Partition Name'})

#or any kind of weird combination like
model.refresh([{<Table Class>:<Partition Class>,'Table Name':['Partition1','Partition2']},'Table Name','Table Name2'])

#You can even run through the Tables & Partition Attributes
model.Tables['Table Name'].refresh()

#or
model.Tables['Table Name'].Partitions['Partition Name'].refresh()

#Default Tracing happens automatically, but can be removed by... 
model.refresh(['Table1','Table2'], trace = None)
```

It's not uncommon to need to run through some checks on specific Tables, Partitions, Columns, Etc...
```python
#Get Row Count from model
model.Tables['Table Name'].row_count()

#Get Last Refresh time from a partition
model.Tables['Table Name'].last_refresh()

#Get Distinct Count or Values from a Column
model.Tables['Table Name'].Columns['Column Name'].distinct_count()
#or
model.Tables['Table Name'].Columns['Column Name'].values()
```
### Documenting a Model
The Tabular model contains a lot of information that can be used to generation documentation if filled in. Currently the markdown files are generated with the Docusaurs heading in place, but this will be changed in future to support multiple documentation platforms. 

**Tip**: With Tabular Editor 2 (Free) or 3 (Paid) you can easily add Descriptioms, Translations (Cultures) and other additonal information that can later be used for generating the documentation. 

#### Args:
- **model**: Tabular
- **friendly_name**: Default > No Value 

To specify the location of the docs, just supply the save location with a new folder name argument. 
- **save_location**: Default > docs

Each page in the generation process has it's own specific name, with these arguments you can rename them to your liking. 
- **general_page_url**: Default > 1-general-information.md
- **measure_page_url**: Default > 2-measures.md
- **table_page_url**: Default > 3-tables.md
- **column_page_url**: Default > 4-columns.md
- **roles_page_url**: Default > 5-roles.md

#### Documenting a Model
The simpelst way to document a tabular model is to connect to the model, and initialize the documentation and execute `save_documentation()`. 

```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs 
docs = pytabular.ModelDocumenter(model)

# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```

#### Documenting a Model with Cultures
Some model creators choose to add cultures to a tabular model for different kinds of reasons. We can leverage those cultures to use the translation names instead of the original object names. In order to this you can set translations to `True` and specify the culture you want to use (e.g. `'en-US'). 

```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs 
docs = pytabular.ModelDocumenter(model)

# Set the translation for documentation to an available culture.
docs = pytabular.ModelDocumenter(model)

# By setting the Tranlsations to `True` it will check if it exists and if it does, 
# it will start using the translations for the docs
docs.set_transalation(
        enable_translations = True, 
        culture = 'en-US'
    )
    
# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```
#### Documenting a Power BI Desktop Model
The Local model doesn't have a "name", only an Id. So we need to Supply a "Friendly Name", which will be used to store the markdown files. The result of this example with be a folder `my-docs-folder` with a subfolder `Adventure Works` where all the files are stored.
```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs, set a friendly name to store the markdown files and overwrite the default location.
docs = pytabular.ModelDocumenter(
    model = model,
    friendly_name = "Adventure Works", 
    save_location = "my-docs-folder"
)

# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```

### Use Cases

#### If blank table, then refresh table.
This will use the function [Return_Zero_Row_Tables](https://curts0.github.io/PyTabular/Examples/#return_zero_row_tables) and the method [Refresh](https://curts0.github.io/PyTabular/Tabular/#refresh) from the Tabular class.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
tables = model.Tables.find_zero_rows()
if len(tables) > 0:
    model.refresh(tables)
```

#### Sneak in a refresh.
This will use the method [Is_Process](https://curts0.github.io/PyTabular/Tabular/#is_process) and the method [Refresh](https://curts0.github.io/PyTabular/Tabular/#refresh) from the Tabular class. It will check the DMV to see if any jobs are currently running classified as processing.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
if model.is_process():
    #do what you want if there is a refresh happening
else:
    model.refresh(TABLES_OR_PARTITIONS_TO_REFRESH)
```

#### Show refresh times in model.
This will use the function [Table_Last_Refresh_Times](https://curts0.github.io/PyTabular/Examples/#table_last_refresh_times) and the method [Create_Table](https://curts0.github.io/PyTabular/Tabular/#create_table) from the Tabular class. It will search through the model for all tables and partitions and pull the 'RefreshedTime' property from it. It will return results into a pandas dataframe, which will then be converted into an M expression used for a new table.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
df = model.Tables.last_refresh()
model.create_table(df, 'Refresh Times')
```


#### If BPA Violation, then revert deployment.
Uses a few things. First the [BPA Class](https://curts0.github.io/PyTabular/Best%20Practice%20Analyzer/#bpa), then the [TE2 Class](https://curts0.github.io/PyTabular/Tabular%20Editor%202/), and will finish with the [Analyze_BPA](https://curts0.github.io/PyTabular/Tabular/#analyze_bpa) method. Did not want to re-invent the wheel with the amazing work done with Tabular Editor and it's BPA capabilities.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
te2 = pytabular.TabularEditor() #Feel free to input your TE2 File path or this will download for you.
bpa = pytabular.BPA() #Fee free to input your own BPA file or this will download for you from: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
results = model.analyze_bpa(te2.exe,bpa.location)

if len(results) > 0:
    #Revert deployment here!
```

#### Loop through and query Dax files
Let's say you have multiple dax queries you would like to store and run through as checks. The [Query](https://curts0.github.io/PyTabular/Tabular/#query) method on the Tabular class can also take file paths. Can really be any file type as it's just checking os.path.isfile(). But would suggest .dax or .txt. It will read the file that use that as the new Query_str argument.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
LIST_OF_FILE_PATHS = ['C:\\FilePath\\file1.dax','C:\\FilePath\\file1.txt','C:\\FilePath\\file2.dax','C:\\FilePath\\file2.txt']
for file_path in LIST_OF_FILE_PATHS:
    model.query(file_path)
```

#### Advanced Refreshing with Pre and Post Checks
Maybe you are introducing new logic to a fact table, and you need to ensure that a measure checking last month values never changes. To do that you can take advantage of the `Refresh_Check` and `Refresh_Check_Collection` classes (Sorry, I know the documentation stinks right now). But using those you can build out something that would first check the results of the measure, then refresh, then check the results of the measure after refresh, and lastly perform your desired check. In this case the `pre` value matches the `post` value. When refreshing and your pre does not equal post, it would fail and give an assertion error in your logging.
```python
from pytabular import Tabular
from pytabular.refresh import RefreshCheck, RefreshCheckCollection

model = Tabular(CONNECTION_STR)

# This is our custom check that we want to run after refresh.
# Does the pre refresh value match the post refresh value.
def sum_of_sales_assertion(pre, post):
    return pre == post

# This is where we put it all together into the `Refresh_Check` class. Give it a name, give it a query to run, and give it the assertion you want to make.
sum_of_last_month_sales = RefreshCheck(
    'Last Month Sales',
    lambda: model.query("EVALUATE {[Last Month Sales]}")
    ,sum_of_sales_assertion
)

# Here we are adding it to a `Refresh_Check_Collection` because you can have more than on `Refresh_Check` to run.
all_refresh_check = RefreshCheckCollection([sum_of_last_month_sales])

model.Refresh(
    'Fact Table Name',
    refresh_checks = RefreshCheckCollection([sum_of_last_month_sales])
    
)
```

#### Query as Another User
There are plenty of tools that allow you to query as an 'Effective User' inheriting their security when querying. This is an extremely valuable concept built natively into the .Net apis. My only gripe is they were all UI based. This allows you to programmatically connect as an effective user and query in Python. You could easily loop through all your users to run tests on their security.
```python
import pytabular as p

#Connect to your model like usual...
model = p.Tabular(CONNECTION_STR)

#This will be the query I run...
query_str = '''
EVALUATE
SUMMARIZE(
    'Product Dimension',
    'Product Dimension'[Product Name],
    "Total Product Sales", [Total Sales]
)
'''
#This will be the user I want to query as...
user_email = 'user1@company.com'

#Base line, to query as the user connecting to the model.
model.query(query_str)

#Option 1, Connect via connection class...
user1 = p.Connection(model.Server, Effective_User = user_email)
user1.query(query_str)

#Option 2, Just add Effective_User
model.query(query_str, Effective_User = user_email)

#PyTabular will do it's best to handle multiple accounts...
#So you won't have to reconnect on every query
```

#### Refresh Related Tables
Ever need to refresh related tables of a Fact? Now should be a lot easier.
```python
import pytabular as p

#Connect to model
model = p.Tabular(CONNECTION_STR)

#Get related tables
tables = model.Tables[TABLE_NAME].related()

#Now just refresh like usual...
tables.refresh()
```

## Documenting a Model
The Tabular model contains a lot of information that can be used to generation documentation if filled in. Currently the markdown files are generated with the Docusaurs heading in place, but this will be changed in future to support multiple documentation platforms. 

**Tip**: With Tabular Editor 2 (Free) or 3 (Paid) you can easily add Descriptioms, Translations (Cultures) and other additonal information that can later be used for generating the documentation. 

Args:
- **model**: Tabular
- **friendly_name**: Default > No Value 

To specify the location of the docs, just supply the save location with a new folder name argument. 
- **save_location**: Default > docs

Each page in the generation process has it's own specific name, with these arguments you can rename them to your liking. 
- **general_page_url**: Default > 1-general-information.md
- **measure_page_url**: Default > 2-measures.md
- **table_page_url**: Default > 3-tables.md
- **column_page_url**: Default > 4-columns.md
- **roles_page_url**: Default > 5-roles.md

### Documenting a Model
The simpelst way to document a tabular model is to connect to the model, and initialize the documentation and execute `save_documentation()`. 

```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs 
docs = pytabular.ModelDocumenter(model)

# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```

### Documenting a Model with Cultures
Some model creators choose to add cultures to a tabular model for different kinds of reasons. We can leverage those cultures to use the translation names instead of the original object names. In order to this you can set translations to `True` and specify the culture you want to use (e.g. `'en-US'). 

```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs 
docs = pytabular.ModelDocumenter(model)

# Set the translation for documentation to an available culture.
# By setting the Tranlsations to `True` it will check if it exists and if it does, 
# it will start using the translations for the docs
docs.set_translations(
        enable_translations = True, 
        culture = 'en-US'
    )

# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```
### Documenting a Power BI > Local Model.
The Local model doesn't have a "name", only an Id. So we need to Supply a "Friendly Name", which will be used to store the markdown files.
```python
import pytabular

# Connect to a Tabular Model Model
model = pytabular.Tabular(CONNECTION_STR)

# Initiate the Docs and set a friendly name to store the markdown files.
docs = pytabular.ModelDocumenter(
    model = model,
    friendly_name = "Adventure Works"
)

# Generate the pages. 
docs.generate_documentation_pages()

# Save docs to the default location
docs.save_documentation()
```
### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)
