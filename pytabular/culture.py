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
        self.ObjectTranslations = PyObjectTranslations(
            [
                PyObjectTranslation(translation, self)
                for translation in self._object.ObjectTranslations.GetEnumerator()
            ]
        )

    def get_translation(self, object_name: str, parent_object: str, object_type = 'Caption') -> dict:
        caption = self.ObjectTranslations.__getitem__(object_name)
        object_translation = caption.Value
        display_folder_translation = caption.Value
        return {
            "Object Translation": object_translation, 
            "Display Folder Translation": display_folder_translation
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
