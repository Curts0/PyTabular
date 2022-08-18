import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
logging.debug('Logging configured...')

logging.debug(f'Setting up file paths for {__file__}')
import os
import sys
dll = os.path.join(os.path.dirname(__file__),"dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))

logging.debug(f'Beginning CLR references...')
import clr
logging.debug('Adding Reference Microsoft.AnalysisServices.AdomdClient')
clr.AddReference('Microsoft.AnalysisServices.AdomdClient')
logging.debug('Adding Reference Microsoft.AnalysisServices.Tabular')
clr.AddReference('Microsoft.AnalysisServices.Tabular')
logging.debug('Adding Reference Microsoft.AnalysisServices')
clr.AddReference('Microsoft.AnalysisServices')

logging.debug(f"Importing from the rest...")
from . pytabular import Tabular, BPA, TE2
from . basic_checks import Return_Zero_Row_Tables, Table_Last_Refresh_Times, BPA_Violations_To_DF
from . logic_utils import pd_dataframe_to_m_expression, pandas_datatype_to_tabular_datatype
from . tabular_tracing import Base_Trace, Refresh_Trace