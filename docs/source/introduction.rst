Introduction
============

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains methods to define inventories of radionuclides, to decay them over
time, and to output radioactive decay data.

The orignal idea was to create a light weight and fast Python package for
radioactive decay modelling, with full support for decay chains, branching and
metastable states. Currently, ``radioactivedecay`` uses the decay data from
`ICRP 107 <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_ by
default. It solves the decay chain differential equations analytically using a
`matrix algebra solution <https://doi.org/10.1088/0952-4746/26/3/N02>`_
:ref:`[1] <refs>`.

In order to use ``radioactivedecay``, you will need Python 3.6+, NumPy and
SciPy. The code is platform independent and has been confirmed as working on
Windows, MacOS and Linux.

Contributors
------------

* `Alex Malins <https://alexmalins.com>`_

Acknowledgements
----------------

Special thanks to:

* `Center for Computational Science & e-Systems <https://ccse.jaea.go.jp/index_eng.html>`_ in JAEA
* `Kenny McKee <https://github.com/Rolleroo>`_

.. _refs:

References
----------

1. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010) `10.1088/0952-4746/26/3/N02 <https://doi.org/10.1088/0952-4746/26/3/N02>`_
