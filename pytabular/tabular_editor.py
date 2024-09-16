"""This has a `Tabular_Editor` class which will download TE2 from a default location.

Or you can input your own location.
"""

import logging
import os
import requests as r
import zipfile as z
import atexit
from logic_utils import remove_folder_and_contents

logger = logging.getLogger("PyTabular")


def download_tabular_editor(
    download_location: str = (
        "https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip"  # noqa: E501
    ),
    folder: str = "Tabular_Editor_2",
    auto_remove=True,
    verify=False,
) -> str:
    """Runs a request.get() to retrieve the zip file from web.

    Will unzip response and store in directory.
    Will also register the removal of the new directory
    and files when exiting program.

    Args:
            download_location (str, optional): File path for zip of Tabular Editor 2.
                    See code args for default download url.
            folder (str, optional): New Folder Location. Defaults to "Tabular_Editor_2".
            auto_remove (bool, optional): Boolean to determine auto
                    removal of files once script exits. Defaults to True.
            verify (bool, optional): Passthrough argument for `r.get`. Need to update later.

    Returns:
            str: File path of TabularEditor.exe
    """
    logger.info("Downloading Tabular Editor 2...")
    logger.info(f"From... {download_location}")
    folder_location = os.path.join(os.getcwd(), folder)
    response = r.get(download_location, verify=verify)
    file_location = f"{os.getcwd()}\\{download_location.split('/')[-1]}"
    with open(file_location, "wb") as te2_zip:
        te2_zip.write(response.content)
    with z.ZipFile(file_location) as zipper:
        zipper.extractall(path=folder_location)
    logger.debug("Removing Zip File...")
    os.remove(file_location)
    logger.info(f"Tabular Editor Downloaded and Extracted to {folder_location}")
    if auto_remove:
        logger.debug(f"Registering removal on termination... For {folder_location}")
        atexit.register(remove_folder_and_contents, folder_location)
    return f"{folder_location}\\TabularEditor.exe"


class TabularEditor:
    """Setting Tabular_Editor Class for future work.

    Mainly runs `download_tabular_editor()`
    """

    def __init__(
        self, exe_file_path: str = "Default", verify_download: bool = True
    ) -> None:
        """Init for `TabularEditor()` class.

        This is mostly a placeholder right now.
        But useful if you want an easy way to download TE2.

        Args:
            exe_file_path (str, optional): File path where TE2 lives. Defaults to "Default".
                If "Default", it will run `download_tabular_editor()`
                and download from github.
            verify_download (bool, optional): Passthrough argument for `r.get`. Need to update later.
        """
        logger.debug(f"Initializing Tabular Editor Class:: {exe_file_path}")
        if exe_file_path == "Default":
            self.exe: str = download_tabular_editor(verify=verify_download)
        else:
            self.exe: str = exe_file_path
        pass
