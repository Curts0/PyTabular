# flake8: noqa
import logging
import os
import sys
import platform

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s::%(module)s::%(funcName)s::%(levelname)s::%(message)s",
    datefmt="%y/%m/%d %H:%M:%S %z",
)
logger = logging.getLogger("PyTabular")
logger.setLevel(logging.INFO)
logger.info("Logging configured...")
logger.info(f"To update PyTabular logger...")
logger.info(f">>> import logging")
logger.info(f">>> pytabular.logger.setLevel(level=logging.INFO)")
logger.info(f"See https://docs.python.org/3/library/logging.html#logging-levels")


logger.debug(f"Python Version::{sys.version}")
logger.debug(f"Python Location::{sys.exec_prefix}")
logger.debug(f"Package Location::{__file__}")
logger.debug(f"Working Directory::{os.getcwd()}")
logger.debug(f"Platform::{sys.platform}-{platform.release()}")

dll = os.path.join(os.path.dirname(__file__), "dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))

logger.debug(f"Beginning CLR references...")
import clr

logger.info("Adding Reference Microsoft.AnalysisServices.AdomdClient")
clr.AddReference("Microsoft.AnalysisServices.AdomdClient")
logger.info("Adding Reference Microsoft.AnalysisServices.Tabular")
clr.AddReference("Microsoft.AnalysisServices.Tabular")
logger.info("Adding Reference Microsoft.AnalysisServices")
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

logger.debug(f"Import successful...")
