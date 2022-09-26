import logging
import requests as r
import atexit
import json
import os
from logic_utils import remove_folder_and_contents


logger = logging.getLogger("PyTabular")


def Download_BPA_File(
    Download_Location: str = "https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json",
    Folder: str = "Best_Practice_Analyzer",
    Auto_Remove=True,
) -> str:
    """Runs a request.get() to retrieve the json file from web. Will return and store in directory. Will also register the removal of the new directory and file when exiting program.

    Args:
            Download_Location (_type_, optional): F. Defaults to [Microsoft GitHub BPA]'https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json'.
            Folder (str, optional): New Folder String. Defaults to 'Best_Practice_Analyzer'.
            Auto_Remove (bool, optional): If you wish to Auto Remove when script exits. Defaults to True.

    Returns:
            str: File Path for the newly downloaded BPA.
    """
    logger.info(f"Downloading BPA from {Download_Location}")
    folder_location = os.path.join(os.getcwd(), Folder)
    if os.path.exists(folder_location) is False:
        os.makedirs(folder_location)
    response = r.get(Download_Location)
    file_location = os.path.join(folder_location, Download_Location.split("/")[-1])
    with open(file_location, "w", encoding="utf-8") as bpa:
        json.dump(response.json(), bpa, ensure_ascii=False, indent=4)
    if Auto_Remove:
        logger.debug(f"Registering removal on termination... For {folder_location}")
        atexit.register(remove_folder_and_contents, folder_location)
    return file_location


class BPA:
    """Setting BPA Class for future work..."""

    def __init__(self, File_Path: str = "Default") -> None:
        logger.debug(f"Initializing BPA Class:: {File_Path}")
        if File_Path == "Default":
            self.Location: str = Download_BPA_File()
        else:
            self.Location: str = File_Path
        pass
