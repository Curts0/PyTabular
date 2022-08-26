
# PyTabular
[![PyPI version](https://badge.fury.io/py/python-tabular.svg)](https://badge.fury.io/py/python-tabular)
[![readthedocs](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/readthedocs.yml)
[![pages-build-deployment](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Curts0/PyTabular/actions/workflows/pages/pages-build-deployment)

### What is it?

PyTabular is a python package that allows for programmatic execution on your tabular models! This is possible thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). The package should have the dll files included when you import it. See [Documentation Here](https://curts0.github.io/PyTabular/). PyTabular is still considered alpha while I'm working on building out the proper tests and testing environments, so I can ensure some kind of stability in features.

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
    
    #Example Dax Query
    #EVALUATE
    #TOPN(100,'Table1')

    # Returns a Pandas DataFrame
```

See [Refresh Tables and Partitions](https://curts0.github.io/PyTabular/Tabular/#refresh).

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

Built In Dax Query Helpers. In-case you want to run some quick queries similar to what vertipaq analyzer will do when getting row counts.
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

Backup & Revert a Table in Memory. USE WITH CAUTION, obviously not in PROD. I have been experimenting with this concept. 
```python
    model.Backup_Table('TableName') #This will backup the table with surround items (columns,measures,relationships,roles,hierarchies,etc.) and will add a suffix of '_backup'
    #Make any changes to your original table and then revert or delete backup as necessary
    model.Revert_Table('TableName') #This will essentially replace your original with _backup
```

Run BPA from TE2. Roadmap to make this more robust, and allow you to run all the command line interfaces that TE2 has to offer.
```python
    TE2 = pytabular.TE2() #Feel free to input your TE2 File path or this will download for you.
    BPA = pytabular.BPA() #Fee free to input your own BPA file or this will download for you from: https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json
    model.Analyze_BPA(TE2.EXE_Path,BPA.Location) #This will output a list of BPA violations...
```