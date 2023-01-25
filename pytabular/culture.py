"""`culture.py` is used to house the `PyCulture`, `PyCultures`, and `PyObjectTranslations` classes.
"""
import logging
from object import PyObject, PyObjects

logger = logging.getLogger("PyTabular")


class PyCulture(PyObject):
    """Wrapper for [Cultures](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.culture?view=analysisservices-dotnet).

    Args:
        Table: Parent Table to the Object Translations
    """

    def __init__(self, object, model) -> None:
        super().__init__(object)
        self.Model = model
        self._display.add_row("Culture Name", self._object.Name)
        self.ObjectTranslations = self.set_translation()

    def set_translation(self) -> list[dict]:
        return [
            {
                "object_translation": translation.Value,
                "object_name": translation.Object.Name,
                "object_parent_name": translation.Object.Parent.Name,
                "object_type": str(translation.Property),
            }
            for translation in self._object.ObjectTranslations
        ]

    def get_translation(
        self, object_name: str, object_parent_name: str, object_type: str = "Caption"
    ) -> dict:
        if translations := [
            d
            for d in self.ObjectTranslations
            if d["object_name"] == object_name
            and d["object_type"] == object_type
            and d["object_parent_name"] == object_parent_name
        ]:
            return translations[0]

        return {"object_not_found": "Not Available"}


class PyCultures(PyObjects):
    """Houses grouping of `PyCulture`."""

    def __init__(self, objects) -> None:
        super().__init__(objects)
