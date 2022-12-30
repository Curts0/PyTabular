import logging
from object import PyObject, PyObjects

logger = logging.getLogger("PyTabular")


class PyCulture(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Cultures]

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


class PyObjectTranslation(PyObject):
    """Wrapper for [Microsoft.AnalysisServices.Cultures]
    Args:
        Table: Child item of the Culture.
    """

    def __init__(self, object, culture) -> None:
        self.Name = object.Object.Name
        self.ObjectType = object.Object.ObjectType
        self.Parent = object.Object.Parent
        super().__init__(object)
        self.Culture = culture
        self._display.add_row("Object Property", str(self._object.Property))
        self._display.add_row("Object Value", self._object.Value)


class PyCultures(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)


class PyObjectTranslations(PyObjects):
    def __init__(self, objects) -> None:
        super().__init__(objects)
