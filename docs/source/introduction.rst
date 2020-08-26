Introduction
============

Overview
--------

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains methods to define inventories of radionuclides, to perform
radioactive decay calculations, and to output radioactive decay data.

The orignal concept was to create a relatively simple and light weight Python
package for radioactive decay calculations, but with full support for branching
and multi-step decay chains, including those which pass through metastable
states. Currently ``radioactivedecay`` uses the decay data from ICRP 107
:ref:`[1] <refs>` by default. It solves the decay chain differential equations
analytically using matrix multiplications :ref:`[2] <refs>`.

In order to use ``radioactivedecay``, you will need Python 3.6+ with NumPy and
SciPy installed. The code is platform independent and has been confirmed to
work on Windows, MacOS and Linux.

Quick Start
-----------

Install ``radioactivedecay`` via the command:

.. code-block:: bash

    $ pip install radioactivedecay

Import the Python package and decay a simple inventory by:

.. code-block:: python3

    >>> import radioactivedecay as rd
    >>> inv = rd.Inventory({'H-3': 1.0})
    >>> inv.contents
    {'H-3': 1.0}
    >>> decayed_inv = inv.decay(12.32, 'y')
    >>> decayed_inv.contents
    {'H-3': 0.5}

The half-life of H-3 (tritium) is 12.32 years, so in this example the activity
reduced by a factor of two.

License
-------

.. include:: <isonum.txt>

``radioactivedecay`` is open source software released under the `MIT 
<https://github.com/alexmalins/radioactivedecay/blob/master/LICENSE>`_ licence.
It uses the  ICRP 107 decay data :ref:`[1] <refs>`, which is Copyright |copy|
2008 A. Endo and K.F. Eckerman.

Contributors
------------

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
