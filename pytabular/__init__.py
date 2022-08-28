import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
logger = logging.getLogger('PyTabular')
logger.setLevel(logging.DEBUG)
logger.debug('Logging configured...')
logger.debug(f'To update PyTabular logger...')
logger.debug(f'>>> import logging')
logger.debug(f'>>> pytabular.logger.setLevel(level=logging.INFO)')
logger.debug(f'Visit https://docs.python.org/3/library/logging.html#logging-levels for info...')

logger.debug(f'Setting up file paths for {__file__}')
import os
import sys
dll = os.path.join(os.path.dirname(__file__),"dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))

logger.debug(f'Beginning CLR references...')
import clr
logger.debug('Adding Reference Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
logger.debug('Adding Reference Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
logger.debug('Adding Reference Microsoft.AnalysisServices')
clr.AddReference('Microsoft.AnalysisServices')

logger.debug(f"Importing specifics in module...")
from . pytabular import Tabular
from . basic_checks import Return_Zero_Row_Tables, Table_Last_Refresh_Times, BPA_Violations_To_DF, Last_X_Interval
from . logic_utils import pd_dataframe_to_m_expression, pandas_datatype_to_tabular_datatype
from . tabular_tracing import Base_Trace, Refresh_Trace
from . tabular_editor import Tabular_Editor
from . best_practice_analyzer import BPA
logging.debug(f'Import successful...')