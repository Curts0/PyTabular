# PyTabular
[![PyPI version](https://badge.fury.io/py/python-tabular.svg)](https://badge.fury.io/py/python-tabular)
[![Downloads](https://pepy.tech/badge/python-tabular)](https://pepy.tech/project/python-tabular)
[![readthedocs](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml)
[![pages-build-deployment](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment)
[![flake8](https://github.com/Curts0/PyTabular/actions/workflows/flake8.yml/badge.svg?branch=master)](https://github.com/Curts0/PyTabular/actions/workflows/flake8.yml)
[![docstr-coverage](https://github.com/Curts0/PyTabular/actions/workflows/docstr-coverage.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/docstr-coverage.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
### What is it?

[PyTabular](https://github.com/Curts0/PyTabular) (**python-tabular** in [pypi](https://pypi.org/project/python-tabular/)) is a python package that allows for programmatic execution on your tabular models! This is possible thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). Currently this build is tested and working on **Windows Operating System only**. Help is needed to expand this for other os. See the [Documentation Here](https://curts0.github.io/PyTabular/). PyTabular is still considered alpha. Please send bugs my way! Preferably in the issues section in Github.

### Getting Started
See the [Pypi project](https://pypi.org/project/python-tabular/) for available versions. **To become PEP8 compliant with naming conventions, serious name changes were made in 0.3.5.** Install v. 0.3.4 or lower to get the older naming conventions.
```powershell title="Install Example"
python3 -m pip install python-tabular

#install specific version
python3 -m pip install python-tabular==0.3.4
```

In your python environment, import pytabular and call the main Tabular Class. Only parameter needed is a solid connection string.
```python title="Connecting to Model"
import pytabular
model = pytabular.Tabular(CONNECTION_STR) # (1)
```

1. That's it. A solid connection string.

You may have noticed some logging into your console. I'm a big fan of logging, if you don't want any just get the logger and disable it.
```python title="Logging Example"
import pytabular
pytabular.logger.disabled = True
```

You can query your models with the `query()` method from your tabular class. For Dax Queries, it will need the full Dax syntax. See [EVALUATE example](https://dax.guide/st/evaluate/). This will return a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html). If you are looking to return a single value, see below. Simply wrap your query in the the curly brackets. The method will take that single cell table and just return the individual value. You can also query your DMV. See below for example.
```python title="Query Examples"
#Run basic queries
DAX_QUERY = "EVALUATE TOPN(100, 'Table1')"
model.query(DAX_QUERY) # (1)

#or...
DMV_QUERY = "select * from $SYSTEM.DISCOVER_TRACE_EVENT_CATEGORIES"
model.query(DMV_QUERY) # (2)

#or...
SINGLE_VALUE_QUERY_EX = "EVALUATE {1}"
model.query(SINGLE_VALUE_QUERY_EX) # (3)

#or...
FILE_PATH = 'C:\\FILEPATHEXAMPLE\\file.dax'
model.query(FILE_PATH) # (4)
```

1. Returns a `pd.DataFrame()`.
2. Returns a `pd.DataFrame()`.
3. This will return a single value. Example, `1` or `'string'`.
4. This will return same logic as above, single values if possible else will return `pd.DataFrame()`. Supply any file type.


You can also explore your tables, partitions, columns, etc. via the attributes of your `Tabular` class.
```python title="Usage Examples"
model.Tables['Table Name'].refresh() # (1)

#or
model.Tables['Table Name'].Partitions['Partition Name'].refresh() # (2)

#or
model.Tables['Table Name'].Partitions[4].last_refresh() # (3)

#or
model.Tables['Table Name'].row_count() # (4)

#or
model.Tables['Table Name'].Columns['Column Name'].distinct_count() # (5)
```

1. Refresh a specific table. The `.Tables` is your attribute to gain access to your `PyTables` class. From that, you can iterate into specific `PyTable` classes.
2. Refresh a specific partition.
3. Get the last refresh time of a specific partition. Notice this time that instead of the partition name, an `int` was used to index into the specific `PyPartition`.
4. Get row count of a table.
5. Get distinct count of a column.

Use the `refresh()` method to handle refreshes on your model. This is synchronous. Should be flexible enough to handle a variety of inputs. See [PyTabular Docs for Refreshing Tables and Partitions](https://curts0.github.io/PyTabular/refresh). Most basic way to refresh is input the table name string. The method will search for table and output exception if unable to find it. For partitions you will need a key, value combination. Example, `{'Table1':'Partition1'}`. You can also take the key value pair and iterate through a group of partitions. Example, `{'Table1':['Partition1','Partition2']}`. Rather than providing a string, you can also input the actual class. See below for those examples. You can acess them from the built in attributes `self.Tables`, `self.Partitions`.
```python title="Refresh Examples"
model.refresh('Table Name') # (1)

model.refresh(['Table1','Table2','Table3']) # (2)

#or...
model.refresh(<PyTable Class>) # (3)

#or...
model.refresh(<PyPartition Class>) # (4)

#or...
model.refresh({'Table Name':'Partition Name'}) # (5)

#or...
model.refresh(
    [
        {
            <PyTable Class>:<PyPartition Class>,
            'Table Name':['Partition1','Partition2']
        },
        'Table Name',
        'Table Name2'
    ]
) # (6)

#or...
model.Tables['Table Name'].refresh() # (7)

#or...
model.Tables['Table Name'].Partitions['Partition Name'].refresh() # (8)

#or...
model.refresh(['Table1','Table2'], trace = None) # (9)
```

1. Basic refresh of a specific table by table name string.
2. Basic refresh of a group of tables by table name strings. Example is with list, but as long as it's iterable you should be fine.
3. Refresh of a table by passing the `PyTable` class.
4. Refresh of a partition by passing the `PyPartition` class.
5. Refresh a specific partition by passing a dictionary with table name as key and partition name as value.
6. Get crazy. Pass all kinds of weird combinations.
7. Basic refresh from a `PyTable` class.
8. Basic refresh from a `PyPartition` class.
9. By default a `RefreshTrace` is started during refresh. It can be disabled by setting `trace = None`.

### Use Cases

#### If blank table, then refresh table.
This will use the function [find_zero_rows](https://curts0.github.io/PyTabular/PyTables/#pytabular.table.PyTables.find_zero_rows) and the method [refresh](https://curts0.github.io/PyTabular/PyTables/#pytabular.table.PyTables.refresh) from the Tabular class.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
tables = model.Tables.find_zero_rows()
if len(tables) > 0:
    tables.refresh()
```

Maybe you only want to check a subset of tables? Like `find()` tables with 'fact' in the name, then check if any facts are blank.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
tables = model.Tables.find('fact').find_zero_rows()
if len(tables) > 0:
    tables.refresh()
```

#### Sneak in a refresh.
This will use the method [is_process](https://curts0.github.io/PyTabular/Tabular/#pytabular.pytabular.Tabular.is_process) and the method [refresh](https://curts0.github.io/PyTabular/Tabular/#pytabular.pytabular.Tabular.refresh) from the Tabular class. It will check the DMV to see if any jobs are currently running classified as processing.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
if model.is_process():
    #do what you want if there is a refresh happening
else:
    model.refresh(TABLES_OR_PARTITIONS_TO_REFRESH)
```

#### Show refresh times in model.
This will use the function [last_refresh](https://curts0.github.io/PyTabular/PyTables/#pytabular.table.PyTables.last_refresh) and the method [create_table](https://curts0.github.io/PyTabular/Tabular/#pytabular.pytabular.Tabular.create_table) from the Tabular class. It will search through the model for all tables and partitions and pull the 'RefreshedTime' property from it. It will return results into a pandas dataframe, which will then be converted into an M expression used for a new table.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
df = model.Tables.last_refresh()
model.create_table(df, 'Refresh Times')
```


#### If BPA Violation, then revert deployment.
This uses a few things. First the [BPA Class](https://curts0.github.io/PyTabular/best_practice_analyzer/), then the [TE2 Class](https://curts0.github.io/PyTabular/tabular_editor/), and will finish with the [analyze_bpa](https://curts0.github.io/PyTabular/Tabular/#pytabular.pytabular.Tabular.analyze_bpa) method. Did not want to re-invent the wheel with the amazing work done with Tabular Editor and it's BPA capabilities.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
# Feel free to input your TE2 File path or this will download for you.
te2 = pytabular.TabularEditor()
# Feel free to input your own BPA file or this will download for you from:
# https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
bpa = pytabular.BPA()
results = model.analyze_bpa(te2.exe,bpa.location)

if len(results) > 0:
    #Revert deployment here!
```

#### Loop through and query Dax files
Let's say you have multiple dax queries you would like to store and run through as checks. The [query](https://curts0.github.io/PyTabular/query/#pytabular.query.Connection.query) method on the Tabular class can also take file paths. It can really be any file type as it's just checking os.path.isfile(). But would suggest `.dax` or `.txt`. It will read the file and use that as the new `query_str` argument.
```python
import pytabular
model = pytabular.Tabular(CONNECTION_STR)
LIST_OF_FILE_PATHS = [
    'C:\\FilePath\\file1.dax',
    'C:\\FilePath\\file1.txt',
    'C:\\FilePath\\file2.dax',
    'C:\\FilePath\\file2.txt'
]
for file_path in LIST_OF_FILE_PATHS:
    model.query(file_path)
```

#### Advanced Refreshing with Pre and Post Checks
Maybe you are introducing new logic to a fact table, and you need to ensure that a measure checking last month values never changes. To do that you can take advantage of the `RefreshCheck` and `RefreshCheckCollection` classes. But using those you can build out something that would first check the results of the measure, then refresh, then check the results of the measure after refresh, and lastly perform your desired check. In this case the `pre` value matches the `post` value. When refreshing, if your pre does not equal post, it would fail and give an assertion error in your logging.
```python
from pytabular import Tabular
from pytabular.refresh import RefreshCheck, RefreshCheckCollection

model = Tabular(CONNECTION_STR)

# This is our custom check that we want to run after refresh.
# Does the pre refresh value match the post refresh value.
def sum_of_sales_assertion(pre, post):
    return pre == post

# This is where we put it all together into the `RefreshCheck` class. Give it a name, give it a query to run, and give it the assertion you want to make.
sum_of_last_month_sales = RefreshCheck(
    'Last Month Sales',
    lambda: model.query("EVALUATE {[Last Month Sales]}")
    ,sum_of_sales_assertion
)

# Here we are adding it to a `RefreshCheckCollection` because you can have more than on `Refresh_Check` to run.
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
user1 = p.Connection(model.Server, effective_user = user_email)
user1.query(query_str)

#Option 2, Just add Effective_User
model.query(query_str, effective_user = user_email)

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
Some model creators choose to add cultures to a tabular model for different kinds of reasons. We can leverage those cultures to use the translation names instead of the original object names. In order to this you can set translations to `True` and specify the culture you want to use (e.g. `'en-US'`). 

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
See [contributing.md](CONTRIBUTING.md)
