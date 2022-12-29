from abc import ABC
from rich.console import Console
from rich.table import Table
from collections.abc import Iterable


class PyObject(ABC):
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
        Console().print(self._display)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        else:
            return getattr(self._object, attr)


class PyObjects:
    def __init__(self, objects) -> None:
        self._objects = objects
        self._display = Table(title=str(self.__class__.mro()[0]))
        for index, obj in enumerate(self._objects):
            self._display.add_row(str(index), obj.Name)

    def __rich_repr__(self) -> str:
        Console().print(self._display)

    def __getitem__(self, object):
        if isinstance(object, str):
            return [pyobject for pyobject in self._objects if object == pyobject.Name][
                -1
            ]
        else:
            return self._objects[object]

    def __iter__(self):
        for object in self._objects:
            yield object

    def __len__(self):
        return len(self._objects)

    def __iadd__(self, obj):
        if isinstance(obj, Iterable):
            self._objects.__iadd__(obj._objects)
        else:
            self._objects.__iadd__([obj])

        self.__init__(self._objects)
        return self

    def Find(self, object_str):
        items = [
            object
            for object in self._objects
            if object_str.lower() in object.Name.lower()
        ]
        return self.__class__.mro()[0](items)
