"""
``radioactivedecay`` is a Python package for radioactive decay calculations.
It supports decay chains of radionuclides, metastable states and branching
decays. By default it uses the decay data from ICRP Publication 107, which
contains 1252 radionuclides of 97 elements.

It solves the radioactive decay differential equations analytically using NumPy
and SciPy linear algebra routines. There is also a high numerical precision
mode using SymPy routines which gives more accurate results for decay chains
with orders of magnitude differences between radionuclide half-lives.
"""

__version__ = "0.2.3"

from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.radionuclide import Radionuclide
from radioactivedecay.inventory import Inventory
