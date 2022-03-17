.. radioactivedecay documentation master file, created by
   sphinx-quickstart on Mon Jul 20 15:32:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to radioactivedecay's documentation!
============================================

.. image:: images/radioactivedecay.png
  :width: 500

``radioactivedecay`` is a Python package for radioactive decay calculations.
It supports decay chains of radionuclides, metastable states and branching
decays. By default it uses the decay data from ICRP Publication 107, which
contains 1252 radionuclides of 97 elements, and atomic mass data from the
Atomic Mass Data Center.

The code solves the radioactive decay differential equations analytically using
NumPy and SciPy linear algebra routines. There is also a high numerical
precision calculation mode employing SymPy routines. This gives more accurate
results for decay chains containing radionuclides with orders of magnitude
differences between the half-lives.

This is free-to-use open source software. It was created for engineers,
technicians and researchers who work with radioactivity, and for
educational use.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   overview
   installation
   tutorial
   plotting
   theory
   api

..
   Indices and tables
..
   ==================
..
   * :ref:`genindex`
..
   * :ref:`modindex`
..
   * :ref:`search`
