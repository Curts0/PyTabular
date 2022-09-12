#


### Return_Zero_Row_Tables
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L9)
```python
.Return_Zero_Row_Tables(
   model: pytabular.Tabular
)
```

---
Returns list of table names of those that are returning isna()


**Args**

* **model** (pytabular.Tabular) : Tabular Model


**Returns**

* List of table names where DAX COUNTROWS('Table Name') is nan or 0.


----


### Table_Last_Refresh_Times
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L23)
```python
.Table_Last_Refresh_Times(
   model: pytabular.Tabular, group_partition: bool = True
)
```

---
Returns pd.DataFrame of tables with their latest refresh time. 
Optional 'group_partition' variable, default is True.
If False an extra column will be include to have the last refresh time to the grain of the partition
Example to add to model model.Create_Table(p.Table_Last_Refresh_Times(model),'RefreshTimes')


**Args**

* **model** (pytabular.Tabular) : Tabular Model
* **group_partition** (bool, optional) : Whether or not you want the grain of the dataframe to be by table or by partition. Defaults to True.


**Returns**

* **DataFrame**  : pd dataframe with the RefreshedTime property: https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.partition.refreshedtime?view=analysisservices-dotnet#microsoft-analysisservices-tabular-partition-refreshedtime
If group_partition == True and the table has multiple partitions, then df.groupby(by["tables"]).max()

----


### BPA_Violations_To_DF
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L51)
```python
.BPA_Violations_To_DF(
   model: pytabular.Tabular, te2: str, bpa: str
)
```

---
Runs BPA Analyzer from TE2 and outputs result into a DF.


**Args**

* **model** (pytabular.Tabular) : Tabular Model Class
* **te2** (str) : TE2 Exe File Path (Can use TE2().EXE_path)
* **bpa** (str) : BPA File Location (Can use BPA().Location)


**Returns**

* **DataFrame**  : Super simple right now. Just splits into two columns.. The object in violation and the rule.


----


### Last_X_Interval
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/basic_checks.py\#L67)
```python
.Last_X_Interval(
   Model: pytabular.Tabular, Measure: Union[str, pytabular.pytabular.Measure],
   Column_Name: Union[str, None] = None,
   Date_Column_Identifier: str = "'Date'[DATE_DTE_KEY]",
   Number_Of_Intervals: int = 90, Interval: str = 'DAY'
)
```

---
Pulls the Last X Interval (Ex Last 90 Days) of a specific measure.


**Args**

* **Model** (pytabular.Tabular) : Tabular Model to perform query on.
* **Measure** (Union[str,pytabular.pytabular.Measure]) : Measure to query. If string, will first check for a measure in the model with that name, otherwise will assume it is a DAX Expression (Ex SUM(FactTable[ColumnValue]) ) and perform that as expression
* **Column_Name** (Union[str,None], optional) : Column Name to be outputted in DataFrame. You can provide your own otherwise will take from the Measure Name. Defaults to "Result".
* **Date_Column_Identifier** (str, optional) : Date column dax identifier. Defaults to "'Date'[DATE_DTE_KEY]".
* **Number_Of_Intervals** (int, optional) : This is used to plug in the variables for [DATESINPERIOD](https://docs.microsoft.com/en-us/dax/datesinperiod-function-dax). Defaults to 90.
* **Interval** (str, optional) : Sames as Number_Of_Intervals. Used to plug in parameters of DAX function [DATESINPERIOD](https://docs.microsoft.com/en-us/dax/datesinperiod-function-dax). Defaults to "DAY". Possible options are "DAY", "MONTH", "QUARTER", and "YEAR"


**Returns**

* **DataFrame**  : Pandas DataFrame of results.

