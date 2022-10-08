import logging
import pandas as pd
from object import PyObject, PyObjects


logger = logging.getLogger("PyTabular")


class PyColumn(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Tabular.Column](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column?view=analysisservices-dotnet).
    With a few other bells and whistles added to it. WIP

    Args:
        Table: Parent Table to the Column
    """

    def __init__(self, object, table) -> None:
        super().__init__(object)
        self.Table = table

    def Distinct_Count(self, No_Blank=False) -> int:
        """Get [DISTINCTCOUNT](https://learn.microsoft.com/en-us/dax/distinctcount-function-dax) of Column.

        Args:
            No_Blank (bool, optional): Ability to call [DISTINCTCOUNTNOBLANK](https://learn.microsoft.com/en-us/dax/distinctcountnoblank-function-dax). Defaults to False.

        Returns:
            int: Number of Distinct Count from column. If `No_Blank == True` then will return number of Distinct Count no blanks.
        """
        func = "DISTINCTCOUNT"
        if No_Blank:
            func += "NOBLANK"
        return self.Table.Model.Adomd.Query(
            f"EVALUATE {{{func}('{self.Table.Name}'[{self.Name}])}}"
        )

    def Values(self) -> pd.DataFrame:
        """Get single column DataFrame of [VALUES](https://learn.microsoft.com/en-us/dax/values-function-dax)

        Returns:
            pd.DataFrame: Single Column DataFrame of Values.
        """
        return self.Table.Model.Adomd.Query(
            f"EVALUATE VALUES('{self.Table.Name}'[{self.Name}])"
        )


class PyColumns(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
