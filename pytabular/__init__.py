# flake8: noqa
import logging
import os
import sys
import platform
from rich.logging import RichHandler
from rich.theme import Theme
from rich.console import Console
from rich import pretty

pretty.install()
console = Console(theme=Theme({"logging.level.warning": "bold reverse red"}))
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[RichHandler(console=console)],
)
logger = logging.getLogger("PyTabular")
logger.setLevel(logging.INFO)
logger.info("Logging configured...")
logger.info(f"To update logging:")
logger.info(f">>> import logging")
logger.info(f">>> pytabular.logger.setLevel(level=logging.INFO)")
logger.info(f"See https://docs.python.org/3/library/logging.html#logging-levels")


logger.info(f"Python Version::{sys.version}")
logger.info(f"Python Location::{sys.exec_prefix}")
logger.info(f"Package Location::{__file__}")
logger.info(f"Working Directory::{os.getcwd()}")
logger.info(f"Platform::{sys.platform}-{platform.release()}")

dll = os.path.join(os.path.dirname(__file__), "dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))

logger.debug(f"Beginning CLR references...")
import clr

logger.debug("Adding Reference Microsoft.AnalysisServices.AdomdClient")
clr.AddReference("Microsoft.AnalysisServices.AdomdClient")
logger.debug("Adding Reference Microsoft.AnalysisServices.Tabular")
clr.AddReference("Microsoft.AnalysisServices.Tabular")
logger.debug("Adding Reference Microsoft.AnalysisServices")
clr.AddReference("Microsoft.AnalysisServices")

logger.debug(f"Importing specifics in module...")
from .pytabular import Tabular
from .basic_checks import (
    Return_Zero_Row_Tables,
    Table_Last_Refresh_Times,
    BPA_Violations_To_DF,
    Last_X_Interval,
)
from .logic_utils import (
    pd_dataframe_to_m_expression,
    pandas_datatype_to_tabular_datatype,
)
from .tabular_tracing import Base_Trace, Refresh_Trace
from .tabular_editor import Tabular_Editor
from .best_practice_analyzer import BPA
from .query import Connection

logger.debug(f"Import successful...")
