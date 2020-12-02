"""
``radioactivedecay`` is a Python package for performing radioactive decay
calculations. It supports full decay chains and branching. By default it uses
decay data from ICRP Publication 107. It solves the decay chain differential
equations analytically using NumPy and SciPy linear algebra routines. There
is also a high numerical precision decay calculation mode based on SymPy
routines.
"""

__version__ = "0.1.0"

from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.radionuclide import Radionuclide
from radioactivedecay.inventory import Inventory
