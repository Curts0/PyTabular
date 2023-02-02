"""
`object.py` stores the main parent classes `PyObject` and `PyObjects`.
These classes are used with the others (Tables, Columns, Measures, Partitions, etc.).
"""
from abc import ABC
from rich.console import Console
from rich.table import Table
from collections.abc import Iterable


class PyObject(ABC):
    """The main parent class for your (Tables, Columns, Measures, Partitions, etc.).
    Notice the magic methods. `__rich_repr__()` starts the baseline for displaying your model.
    It uses the amazing `rich` python package and
    builds your display from the `self._display`.
    `__getattr__()` will check in `self._object`, if unable to find anything in `self`.
    This will let you pull properties from the main .Net class.
    """

    def __init__(self, object) -> None:
        self._object = object
        self._display = Table(title=self.Name)
        self._display.add_column(
            "Properties", justify="right", style="cyan", no_wrap=True
        )
        self._display.add_column("", justify="left", style="magenta", no_wrap=False)

        self._display.add_row("Name", self.Name)
        self._display.add_row("ObjectType", str(self.ObjectType))
        if str(self.ObjectType) not in "Model":
            self._display.add_row("ParentName", self.Parent.Name)
            self._display.add_row(
                "ParentObjectType",
                str(self.Parent.ObjectType),
                end_section=True,
            )

    def __rich_repr__(self) -> str:
        """See [Rich Repr Protocol](https://rich.readthedocs.io/en/stable/pretty.html#rich-repr-protocol)"""
        Console().print(self._display)

    def __getattr__(self, attr):
        """Searches in `self._object`"""
        return getattr(self._object, attr)


class PyObjects:
    """
    The main parent class for grouping your (Tables, Columns, Measures, Partitions, etc.).
    Notice the magic methods. `__rich_repr__()` starts the baseline for displaying your model.
    It uses the amazing `rich` python package and
    builds your display from the `self._display`.
    Still building out the magic methods to give `PyObjects` more flexibility.
    """

    def __init__(self, objects) -> None:
        self._objects = objects
        self._display = Table(title=str(self.__class__.mro()[0]))
        for index, obj in enumerate(self._objects):
            self._display.add_row(str(index), obj.Name)

    def __rich_repr__(self) -> str:
        """See [Rich Repr Protocol](https://rich.readthedocs.io/en/stable/pretty.html#rich-repr-protocol)"""
        Console().print(self._display)

    def __getitem__(self, object):
        """Checks if item is str or int. If string will iterate through and try to find matching name.
        Otherwise, will call into `self._objects[int]` to retrieve item.
        """
        if isinstance(object, str):
            return [pyobject for pyobject in self._objects if object == pyobject.Name][
                -1
            ]
        else:
            return self._objects[object]

    def __iter__(self):
        """Default `__iter__()` to iterate through `PyObjects`."""
        yield from self._objects

    def __len__(self) -> int:
        """Default `__len__()`

        Returns:
            int: Number of PyObject in PyObjects
        """
        return len(self._objects)

    def __iadd__(self, obj):
        """
        Add a `PyObject` or `PyObjects` to your current `PyObjects` class.
        This is useful for building out a custom `PyObjects` class to work with.
        """
        if isinstance(obj, Iterable):
            self._objects.__iadd__(obj._objects)
        else:
            self._objects.__iadd__([obj])

        self.__init__(self._objects)
        return self

    def Find(self, object_str: str):
        """Finds any or all `PyObject` inside of `PyObjects` that match the `object_str`.
        It is case insensitive.

        Args:
            object_str (str): str to lookup in `PyObjects`

        Returns:
            PyObjects: Returns a `PyObjects` class with all `PyObject` where the `PyObject.Name` matches `object_str`.
        """
        items = [
            object
            for object in self._objects
            if object_str.lower() in object.Name.lower()
        ]
        return self.__class__.mro()[0](items)
