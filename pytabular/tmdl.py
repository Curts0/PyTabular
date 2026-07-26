"""TMDL compatibility wrapper."""

from __future__ import annotations

from pathlib import Path

from pytabular._runtime import load_tom


class Tmdl:
    """Serialize or apply TMDL for a ``Tabular`` model."""

    def __init__(self, model):
        self.model = model

    def save_to_folder(self, path: str | Path = "tmdl"):
        """Save a model definition to a TMDL folder."""
        if hasattr(self.model, "save_tmdl"):
            self.model.save_tmdl(path)
            return True

        serializer = load_tom().TmdlSerializer
        database = getattr(self.model, "Database", None)
        if database is not None and hasattr(serializer, "SerializeDatabaseToFolder"):
            serializer.SerializeDatabaseToFolder(database, str(path))
        else:
            serializer.SerializeModelToFolder(self.model._object, str(path))
        return True

    def execute(self, path: str | Path = "tmdl", auto_save: bool = True):
        """Copy a TMDL definition into the current model."""
        serializer = load_tom().TmdlSerializer
        if hasattr(serializer, "DeserializeDatabaseFromFolder"):
            loaded = serializer.DeserializeDatabaseFromFolder(str(path)).Model
        else:
            loaded = serializer.DeserializeModelFromFolder(str(path))
        loaded.CopyTo(self.model._object)
        return self.model.save_changes() if auto_save else True
