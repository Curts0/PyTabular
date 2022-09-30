class PyObject:
    def __init__(self, object) -> None:
        self._object = object

    def __repr__(self) -> str:
        return self.Name

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._object, attr)

class PyObjects:
    def __init__(self, objects) -> None:
        self._objects = objects

    def __repr__(self) -> str:
        return f"{len(self._objects)}"

    def __getitem__(self, object):
        if isinstance(object, str):
            return [
                pyobject
                for pyobject in self._objects
                if object == pyobject.Name
            ][-1]
        else:
            return self._objects[object]
    def __iter__(self):
        for object in self._objects:
            yield object
    def __len__(self):
        return len(self._objects)