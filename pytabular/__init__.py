
import os
import sys
dll = os.path.join(os.path.dirname(__file__),"dll")
sys.path.append(dll)
sys.path.append(os.path.dirname(__file__))
from . pytabular import Tabular, iterator, find