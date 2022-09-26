import logging
import os
import requests as r
import zipfile as Z
import atexit
from logic_utils import remove_folder_and_contents

logger = logging.getLogger("PyTabular")


def Download_Tabular_Editor(
    Download_Location: str = "https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip",
    Folder: str = "Tabular_Editor_2",
    Auto_Remove=True,
) -> str:
    """Runs a request.get() to retrieve the zip file from web. Will unzip response and store in directory. Will also register the removal of the new directory and files when exiting program.

    Args:
            Download_Location (str, optional): File path for zip of Tabular Editor 2. Defaults to [Tabular Editor 2 Github Zip Location]'https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip'.
            Folder (str, optional): New Folder Location. Defaults to 'Tabular_Editor_2'.
            Auto_Remove (bool, optional): Boolean to determine auto removal of files once script exits. Defaults to True.

    Returns:
            str: File path of TabularEditor.exe
    """
    logger.info("Downloading Tabular Editor 2...")
    logger.info(f"From... {Download_Location}")
    folder_location = os.path.join(os.getcwd(), Folder)
    response = r.get(Download_Location)
    file_location = f"{os.getcwd()}\\{Download_Location.split('/')[-1]}"
    with open(file_location, "wb") as te2_zip:
        te2_zip.write(response.content)
    with Z.ZipFile(file_location) as zipper:
        zipper.extractall(path=folder_location)
    logger.debug("Removing Zip File...")
    os.remove(file_location)
    logger.info(f"Tabular Editor Downloaded and Extracted to {folder_location}")
    if Auto_Remove:
        logger.debug(f"Registering removal on termination... For {folder_location}")
        atexit.register(remove_folder_and_contents, folder_location)
    return f"{folder_location}\\TabularEditor.exe"


class Tabular_Editor:
    """Setting Tabular_Editor Class for future work."""

    def __init__(self, EXE_File_Path: str = "Default") -> None:
        logger.debug(f"Initializing Tabular Editor Class:: {EXE_File_Path}")
        if EXE_File_Path == "Default":
            self.EXE: str = Download_Tabular_Editor()
        else:
            self.EXE: str = EXE_File_Path
        pass
