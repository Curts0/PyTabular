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
        self._display.add_row(
            "Description", str(self._object.Description), end_section=True
        )
        self._display.add_row("DataType", str(self._object.DataType))
        self._display.add_row("EncodingHint", str(self._object.EncodingHint))
        self._display.add_row("IsAvailableInMDX", str(self._object.IsAvailableInMDX))
        self._display.add_row("IsHidden", str(self._object.IsHidden))
        self._display.add_row("IsKey", str(self._object.IsKey))
        self._display.add_row("IsNullable", str(self._object.IsNullable))
        self._display.add_row("State", str(self._object.State))
        self._display.add_row("DisplayFolder", str(self._object.DisplayFolder))

    def get_sample_values(self, top_n: int = 3) -> pd.DataFrame:
        """Get sample values of column."""
        column_to_sample = f"'{self.Table.Name}'[{self.Name}]"
        dax_query = f"""EVALUATE
                            TOPNSKIP(
                                {top_n},
                                0,
                                FILTER(
                                    VALUES({column_to_sample}),
                                    NOT ISBLANK({column_to_sample}) && LEN({column_to_sample}) > 0
                                ),
                                1
                            )
                            ORDER BY {column_to_sample}
                    """
        return self.Table.Model.Query(dax_query)

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
