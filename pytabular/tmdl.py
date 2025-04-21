"""See [TMDL Scripting].(https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).

Run `Tmdl(model).save_to_folder()` to save tmdl of model.
Run `Tmdl(model).execute()` to execute a specific set of tmdl scripts.
"""

from Microsoft.AnalysisServices.Tabular import TmdlSerializer


class Tmdl:
    """Specify the specific model you want to use for scripting.

    Args:
        model (Tabular): Initialize with Tabular model.
    """
    def __init__(self, model):
        self.model = model

    def save_to_folder(self, path: str = "tmdl"):
        """Runs `SerializeModelToFolder` from .net library.

        Args:
            path (str, optional): directory where to save tmdl structure.
                Defaults to "tmdl".
        """
        TmdlSerializer.SerializeModelToFolder(self.model._object, path)
        return True

    def execute(self, path: str = "tmdl", auto_save: bool = True):
        """Runs `DeserializeModelFromFolder` from .net library.

        Args:
            path (str, optional): directory to look for tmdl scripts.
                Defaults to "tmdl".
            auto_save (bool, optional): You can set to false
                if you want to precheck a few things, but will need to
                run `model.save_changes()`. Setting to `True` will go ahead
                and execute `model.save_changes()` Defaults to True.
        """
        model_object = TmdlSerializer.DeserializeModelFromFolder(path)
        model_object.CopyTo(self.model._object)
        if auto_save:
            return self.model.save_changes()
        else:
            return True
