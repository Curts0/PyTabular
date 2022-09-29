import logging

from Microsoft.AnalysisServices.Tabular import Table
import pandas as pd

logger = logging.getLogger("PyTabular")


class PyTable:
    '''Wrapper for [Microsoft.AnalysisServices.Tabular](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.table?view=analysisservices-dotnet).
    With a few other bells and whistles added to it.
    '''    
    def __init__(self, table, model) -> None:
        self._table = table
        self.Model = model

    def __repr__(self) -> str:
        return self.Name

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._table, attr)

    def Row_Count(self) -> int:
        '''Method to return count of rows. Simple Dax Query:
        `EVALUATE {COUNTROWS('Table Name')}`

        Returns:
            int: Number of rows using [COUNTROWS](https://learn.microsoft.com/en-us/dax/countrows-function-dax).
        '''        
        return self.Model.Adomd.Query(f"EVALUATE {{COUNTROWS('{self.Name}')}}")

    def Refresh(self, *args, **kwargs) -> pd.DataFrame:
        '''Same method from Model Refresh, you can pass through any extra parameters. For example:
        `Tabular().Tables['Table Name'].Refresh(Tracing = True)`
        Returns:
            pd.DataFrame: Returns pandas dataframe with some refresh details
        '''        
        return self.Model.Refresh(self.Name, *args, **kwargs)


class PyTables(list):
    def __init__(self, tables, model) -> None:
        self._tables = tables
        self.Model = model

    def __repr__(self) -> str:
        return self._tables

    def __getitem__(self, table):
        if isinstance(table, str):
            return [
                pytable
                for pytable in self._tables
                if table == pytable.Name
            ][-1]
        else:
            return self._tables[table]
