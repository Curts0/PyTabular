from typing import Union

from Microsoft.AnalysisServices.Tabular import TmdlSerializer


class Tmdl:
    def __init__(self, model):
        self.model = model

    def save_to_folder(self, path: str = "tmdl") -> bool:
        TmdlSerializer.SerializeModelToFolder(self.model._object, path)
        return True

    def execute(self, path: str = "tmdl", auto_save: bool = True):
        model_object = TmdlSerializer.DeserializeModelFromFolder(path)
        model_object.CopyTo(self.model._object)
        if auto_save:
            return self.model.save_changes()
        else:
            return True
