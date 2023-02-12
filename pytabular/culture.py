"""`culture.py` is used to house the `PyCulture`, and `PyCultures` classes."""
import logging
from object import PyObject, PyObjects
from typing import List

logger = logging.getLogger("PyTabular")


class PyCulture(PyObject):
    """Main class to interact with cultures in model."""

    def __init__(self, object, model) -> None:
        """Mostly extends from `PyObject`. But will add rows to `rich`."""
        super().__init__(object)
        self.Model = model
        self._display.add_row("Culture Name", self._object.Name)
        self.ObjectTranslations = self.set_translation()

    def set_translation(self) -> List[dict]:
        """Based on the culture, it creates a list of dicts with available translations."""
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
        """Get Translation makes it possible to seach a specific translation of an object.

        By default it will search for the "Caption" object type, due to fact that a
        Display folder and Description can also have translations.
        """
        try:
            # Removed walrus operator so it can be compatible with with python versions before 3.8
            translations = [
                d
                for d in self.ObjectTranslations
                if d["object_name"] == object_name
                and d["object_type"] == object_type
                and d["object_parent_name"] == object_parent_name
            ]
            return translations[0]
        except Exception:
            return {"object_not_found": "Not Available"}


class PyCultures(PyObjects):
    """Houses grouping of `PyCulture`."""

    def __init__(self, objects) -> None:
        """Extends `PyObjects` class."""
        super().__init__(objects)
