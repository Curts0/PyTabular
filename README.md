
# PyTabular
[![PyPI version](https://badge.fury.io/py/python-tabular.svg)](https://badge.fury.io/py/python-tabular)
[![readthedocs](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml)
[![pages-build-deployment](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment)

### What is it?

PyTabular is a python package that allows for programmatic execution on your tabular models! This is possible thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). The package should have the dll files included when you import it. See [Documentation Here](https://curts0.github.io/PyTabular/)

### Getting Started

```powershell
python3 -m pip install python_tabular
```

In your python environment, import pytabular and call the main Tabular Class. Only parameter needed is a solid connection string.

```python
    import pytabular
    model = pytabular.Tabular(CONNECTION_STR)
```

DAX Query

```python
    model.Query(DAX_QUERY)
    # Returns a Pandas DataFrame
```

[Refresh Tables and Partitions](https://curts0.github.io/PyTabular/Tabular/#refresh)

```python
    #Can be str(table name only), Table object, Partition object, or an iterable combination of the three.
    model.Refresh('Table Name')
    tables_to_refresh = ['Table Name 1', 'Table Name 2', <Table Class>, <Partition Class>]
    #Queue up the tables and partitions that you want to refresh.
    model.Refresh(tables_to_refresh)
    #NOTE if you monitor the logs you will notice a Trace is executed on the refreshes.
```

Built In Dax Query Helpers
```python

    #Query Every Column
    model.Query_Every_Column() #Will return pd.DataFrame()

    #Query Every Table
    model.Query_Every_Table() #Will return pd.DataFrame()
    
    '''
    NOTE, notice the default values for the query_function argument. 
    Query_Every_Column will get COUNTROWS(VALUES(_))
    and Query_Every_Table() will get COUNTROWS(_)
    with '_' being replaced with the dax identifier to the table or column in question.
    You can replace this str with anything you want. For example output the MIN(_) or MAX(_) of each column rather than the default queries.
    '''
```

Backup & Revert a Table in Memory
```python
    model.Backup_Table('TableName') #This will backup the table with surround items (columns,measures,relationships,roles,hierarchies,etc.) and will add a suffix of '_backup'
    #Make any changes to your original table and then revert or delete backup as necessary
    model.Revert_Table('TableName') #This will essentially replace your original with _backup
```

Run BPA from TE2
```python
    TE2 = pytabular.TE2() #Feel free to input your TE2 File path or this will download for you.
    BPA = pytabular.BPA() #Fee free to input your own BPA file or this will download for you from: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
    model.Analyze_BPA(TE2.EXE_Path,BPA.Location) #This will output a list of BPA violations...
```