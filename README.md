
# PyTabular


### What Does It Do?

PyTabular allows for programmatic execution on your tabular models... In Python!

### How Does It Work?

I basically took my two favorite things Python and Tabular Models and connected the two. Thanks to [Pythonnet (3.0.0a2)](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). The package should have the dll files included when you import the package. 

### Getting Started

Importing package

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

Refresh Tables and Partitions

```python
    #filter down the collection to what you want to refresh
    tables_to_refresh = [table for table in model.Tables if table.get_Name() in ['Table1','Table2','Table3']]
    
    #Queue up the tables and partitions that you want to refresh.
    model.Refresh(tables_to_refresh)

    #Once you are ready, update to execute the refresh
    model.Update()
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