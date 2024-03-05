""" Electical Impedance Tomography library using BIMMS system"""

# Meta information
__title__           = 'tomiBIMMS'
__version__         = '0.0.1'
__date__            = '2023–10–24'
__author__          = 'Thomas Couppey'
__contributors__    = 'Thomas Couppey, Louis Regnacq, Florian Kolbl'
__copyright__       = 'Louis Regnacq'
__license__         = 'CeCILL'

# Public interface
from .results.EIT_results import *
from .protocol.Protocol import *
from .system.tomobimms import *
from .utils.constantsmux import *
