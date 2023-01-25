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
        self.ObjectTranslations = self.set_translation(
            self._object.ObjectTranslations.GetEnumerator()
        )

    def set_translation(self, object_translation):
        return [
            {
                "object_translation": translation.Value,
                "object_name": translation.Object.Name,
                "object_parent_name": translation.Object.Parent.Name,
                "object_type": str(translation.Property),
            }
            for translation in object_translation
        ]

    def get_translation(
        self, object_name: str, object_parent_name: str, object_type="Caption"
    ) -> dict:
        if translations := [
            d
            for d in self.ObjectTranslations
            if d["object_name"] == object_name
            and d["object_type"] == object_type
            and d["object_parent_name"] == object_parent_name
        ]:
            return translations[0]

        return {
            "object_translation": "Not Available",
            "object_name": "Not Available",
            "object_parent_name": "Not Available",
            "object_type": "Not Available",
        }


class PyObjectTranslation(PyObject):
    """Wrapper for [ObjectTranslation](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.objecttranslation?view=analysisservices-dotnet)"""

    def __init__(self, object, culture) -> None:
        self.Name = object.Object.Name
        self.ObjectType = object.Object.ObjectType
        self.CultureProperty = str(self._object.Property)
        self.CultureCaption = self._object.Value
        self.Parent = object.Object.Parent
        super().__init__(object)
        self.Culture = culture
        self._display.add_row("Object Property", str(self._object.Property))
        self._display.add_row("Object Value", self._object.Value)


class PyCultures(PyObjects):
    """Houses grouping of `PyCulture`."""

    def __init__(self, objects) -> None:
        super().__init__(objects)


class PyObjectTranslations(PyObjects):
    """Houses grouping of `PyObjectTranslation`."""

    def __init__(self, objects) -> None:
        super().__init__(objects)
