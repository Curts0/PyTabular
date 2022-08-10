import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
import os
import sys
dll = os.path.join(os.path.dirname(__file__),"dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))
from . pytabular import Tabular, BPA, TE2
from . basic_checks import Return_Zero_Row_Tables, Table_Last_Refresh_Times, BPA_Violations_To_DF
from . logic_utils import pd_dataframe_to_m_expression, pandas_datatype_to_tabular_datatype