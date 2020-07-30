Introduction
============

Overview
--------

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains methods to define inventories of radionuclides, to decay them over
time, and to output radioactive decay data.

The orignal idea was to create a light weight and fast Python package for
radioactive decay modelling, with full support for decay chains, branching and
metastable states. Currently, ``radioactivedecay`` uses the decay data from
`ICRP 107 <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_ :ref:`[1]
<refs>` by default. It solves the decay chain differential equations
analytically using a `matrix algebra solution 
<https://doi.org/10.1016/j.cpc.2009.08.011>`_ :ref:`[2] <refs>`.

In order to use ``radioactivedecay``, you will need Python 3.6+, NumPy and
SciPy. The code is platform independent and has been confirmed as working on
Windows, MacOS and Linux.

Quick Start
-----------

Install ``radioactivedecay`` via the command:

.. code-block:: bash

    $ pip install radioactivedecay

Import the package into Python and decay a simple inventory:

.. code-block:: python3

    >>> import radioactivedecay as rd
    >>> inv = rd.Inventory({'H-3': 1.0})
    >>> inv.contents
    {'H-3': 1.0}
    >>> decayed_inv = inv.decay(12.32, 'y')
    >>> decayed_inv.contents
    {'H-3': 0.5}

Note the half-life of H-3 (tritium) is 12.32 years, so in this example the
activity reduced by a factor of two.

License
-------

.. include:: <isonum.txt>

``radioactivedecay`` is open source software released under the `MIT 
<https://github.com/alexmalins/radioactivedecay/blob/master/LICENSE>`_ licence.
The `ICRP-107 decay data
<https://journals.sagepub.com/doi/suppl/10.1177/ANIB_38_3>`_ :ref:`[1] <refs>`
it uses is Copyright |copy| 2008 A. Endo and K.F. Eckerman.

Contributors
------------

* `Alex Malins <https://alexmalins.com>`_

Acknowledgements
----------------

Special thanks to:

* `Center for Computational Science & e-Systems <https://ccse.jaea.go.jp/index_eng.html>`_, `JAEA <https://www.jaea.go.jp/english>`_.
* `Kenny McKee <https://github.com/Rolleroo>`_

.. _refs:

References
----------

1. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_
2. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
