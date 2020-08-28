Introduction
============

Overview
--------

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains functions to define inventories of radionuclides, perform
radioactive decay calculations, and output decay data for radionuclides and
decay chains.

The orignal concept was to create a simple and light weight Python package for
radioactive decay calculations, with full support for branching and multi-step
decay chains, including those which pass through metastable states. Currently
``radioactivedecay`` uses the decay data from ICRP 107 :ref:`[1] <refs>` by
default. It solves the decay chain differential equations analytically using
linear algebra routines :ref:`[2] <refs>`.

In order to use ``radioactivedecay``, you need Python 3.6+ with the NumPy and
SciPy packages installed. The code is platform independent and has tested on
Windows, MacOS and Linux systems.

Quick Start
-----------

Install ``radioactivedecay`` via the command:

.. code-block:: bash

    $ pip install radioactivedecay
    
This command will also attempt to install NumPy and SciPy if they are not
already in your environment.

Import the ``radioactivedecay`` package and decay a simple inventory using:

.. code-block:: python3

    >>> import radioactivedecay as rd
    >>> inv_t0 = rd.Inventory({'H-3': 10.0})
    >>> inv_t0.contents
    {'H-3': 10.0}
    >>> inv_t1 = inv_t0.decay(12.32, 'y')
    >>> inv_t1.contents
    {'H-3': 5.0}

Here we created an inventory of 10.0 units of tritum (H-3) and decayed it for
12.32 years. As 12.32 years is the half-life of tritium, the activity reduced
by a factor of two, i.e. to 5.0 units.

``radioactivedecay`` is agnostic to activity units: units out are the same as
units in. Thus this example could represent 10.0 Bq of H-3 decaying to 5.0 Bq,
or 10.0 Ci to 5.0 Ci, or whichever is your prefererred activity unit.

License
-------

.. include:: <isonum.txt>

``radioactivedecay`` is open source software released under the `MIT 
<https://github.com/alexmalins/radioactivedecay/blob/master/LICENSE>`_ licence.
It uses a pre-processed version of the ICRP 107 decay data :ref:`[1] <refs>`,
which is Copyright |copy| 2008 A. Endo and K.F. Eckerman.

Developer
----------

* `Alex Malins <https://alexmalins.com>`_

Acknowledgements
----------------

Special thanks to:

* the `Center for Computational Science & e-Systems <https://ccse.jaea.go.jp/index_eng.html>`_ in `JAEA <https://www.jaea.go.jp/english>`_.
* `Kenny McKee <https://github.com/Rolleroo>`_

for their support and assistance to this project.

.. _refs:

References
----------

1. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_
2. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
