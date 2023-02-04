"""
best_practice_analyzer is currently just a POC.
You can call the BPA class to download or specify your own BPA file.
It is used with tabular_editor.py to run BPA.
I did not want to re-invent the wheel,
so just letting TE2 work it's magic.
"""
import logging
import requests as r
import atexit
import json
import os
from logic_utils import remove_folder_and_contents


logger = logging.getLogger("PyTabular")


def download_bpa_file(
    download_location: str = "https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json",
    folder: str = "Best_Practice_Analyzer",
    auto_remove=True,
) -> str:
    """Runs a request.get() to retrieve the json file from web. Will return and store in directory. Will also register the removal of the new directory and file when exiting program.

    Args:
            Download_Location (_type_, optional): F. Defaults to [Microsoft GitHub BPA]'https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json'.
            Folder (str, optional): New Folder String. Defaults to 'Best_Practice_Analyzer'.
            Auto_Remove (bool, optional): If you wish to Auto Remove when script exits. Defaults to True.

    Returns:
            str: File Path for the newly downloaded BPA.
    """
    logger.info(f"Downloading BPA from {download_location}")
    folder_location = os.path.join(os.getcwd(), folder)
    if os.path.exists(folder_location) is False:
        os.makedirs(folder_location)
    response = r.get(download_location)
    file_location = os.path.join(folder_location, download_location.split("/")[-1])
    with open(file_location, "w", encoding="utf-8") as bpa:
        json.dump(response.json(), bpa, ensure_ascii=False, indent=4)
    if auto_remove:
        logger.debug(f"Registering removal on termination... For {folder_location}")
        atexit.register(remove_folder_and_contents, folder_location)
    return file_location


class BPA:
    """Setting BPA Class for future work..."""

    def __init__(self, file_path: str = "Default") -> None:
        """BPA class to be used with the TE2 class.

        Args:
            File_Path (str, optional): See `Download_BPA_File()`. Defaults to "Default".
            If "Default, then will run `Download_BPA_File()` without args.
        """
        logger.debug(f"Initializing BPA Class:: {file_path}")
        if file_path == "Default":
            self.location: str = download_bpa_file()
        else:
            self.location: str = file_path
        pass
