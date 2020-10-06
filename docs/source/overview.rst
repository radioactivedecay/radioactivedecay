Overview
========

Introduction
------------

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains functions to define inventories of radionuclides, perform
decay calculations, and output decay data for radionuclides and decay chains.

The orignal goal was to create a simple and light weight Python package for
radioactive decay calculations, with full support for branching decays and
multi-step decay chains, including those which pass through metastable states.
``radioactivedecay`` uses the decay data from ICRP Publication 107
:ref:`[1] <refs>` by default. It solves the decay chain differential equations
analytically using basic linear algebra operations :ref:`[2] <refs>`.

In order to use ``radioactivedecay``, you will need Python 3.6+ with the NumPy
and SciPy packages installed. The code is platform independent and has been
tested on Windows, MacOS and Linux systems.

Quick Start
-----------

Install ``radioactivedecay`` via the command:

.. code-block:: bash

    $ pip install radioactivedecay
    
This command will also attempt to install NumPy and SciPy if they are not
already present in your environment.

Import the ``radioactivedecay`` package and decay a simple inventory using:

.. code-block:: python3

    >>> import radioactivedecay as rd
    >>> inv_t0 = rd.Inventory({'H-3': 10.0})
    >>> inv_t0.contents
    {'H-3': 10.0}
    >>> inv_t1 = inv_t0.decay(12.32, 'y')
    >>> inv_t1.contents
    {'H-3': 5.0}

Here we created an inventory of 10.0 units of tritum (:sup:`3`\H) and decayed it for
12.32 years. The activity reduced by a factor of two, i.e. to 5.0 units, as
12.32 years is the half-life of tritium,

``radioactivedecay`` is agnostic to activity units: the output units are the
same as the input units. The above example could therefore represent 10.0 Bq of
tritium decaying to 5.0 Bq, or 10.0 Ci to 5.0 Ci, or whichever activity unit
you prefer.

How it works
------------

``radioactivedecay`` calculates an analytical solution to the decay chain
differential equations using matrix and vector multiplications. It implements
the method described in ref. :ref:`[2] <refs>`. It calls NumPy 
:ref:`[3] <refs>` and SciPy :ref:`[4] <refs>` for the matrix operations.

The notebooks folder in the `GitHub repository 
<https://github.com/alexmalins/radioactivedecay>`_ contains some Jupyter
Notebooks for creating the `ICRP 107 decay dataset
<https://github.com/alexmalins/radioactivedecay/notebooks/icrp107_dataset/icrp107_dataset.ipynb>`_
for radioactivedecay, and cross-checks against `PyNE
<https://github.com/alexmalins/radioactivedecay/notebooks/comparisons/pyne/rd_pyne_truncated_compare.ipynb>`_ 
:ref:`[5] <refs>` and `Radiological Toolbox 
<https://github.com/alexmalins/radioactivedecay/notebooks/comparisons/radiological_toolbox_compare.ipynb>`_
:ref:`[6] <refs>`.

Limitations
-----------

At present ``radioactivedecay`` has the following limitations:

* It does not model neutronics, so cannot calculate radioactivity produced
  from neutron-nuclear reactions inducing radioactivity or fission.
* It cannot model external sources of radioactivity input to or removal from an
  inventory over time.
* ``radioactivedecay`` uses double precision floating point numbers for
  calculations. Numerical precision issues can arise for decay chains where the
  half-life of the parent is many orders of magnitude smaller than the half-life
  of one of the progeny. Similarly there can be precision issues when two
  radionuclides in a chain have very similar (or identical) half-lives. Note that
  this latter case does not appear to apply to radionuclides within ICRP 107
  dataset, however. If you need greater numerical precision for your decay
  calculations, you could investigate using the `batemaneq 
  <https://pypi.org/project/batemaneq/>`_ :ref:`[7] <refs>` package which
  supports `arbitrary precision calculations
  <https://bjodah.github.io/blog/posts/bateman-equation.html>`_.
* Care is needed when decaying backwards in time, i.e. supplying a negative
  argument to ``decay()``, as this can also result in numerical instabilities and
  nonsensical results.

There are also some limitations associated with the ICRP 107 decay dataset:

* ICRP 107 does not contain data on branching fractions for radionuclides
  produced from spontaneous fission decays. Thus ``decay()`` calls do not
  calculate the spontaneous fission progeny.
* Decay data is quoted in ICRP 107 with up to 5 significant figures of
  precision. The results of decay calculations will therefore not be more precise
  than this level of precision.
* Uncertainties are not quoted for the radioactive decay data in ICRP 107.
  Uncertainties will vary substantially between radionuclides, e.g. depending on
  how well each radionuclide has been researched in the past. In many cases these
  uncertainties more significant for the results of decay calculations than the
  previous point about the quoted precision of the ICRP 107 decay data.
* There are a few instances where minor decay pathways were not included in
  ICRP 107. Examples include the decays At-219-> Rn-219 (|beta| ~3%),
  Es-250 -> Bk-246 (|alpha| ~1.5%), and U-228 -> Pa-228
  (|epsilon| ~2.5%). For more details see refs. :ref:`[8] <refs>` and
  :ref:`[9] <refs>` on the creation of the ICRP 107 dataset.

License
-------

.. include:: <isonum.txt>

``radioactivedecay`` is open source software released under the `MIT 
<https://github.com/alexmalins/radioactivedecay/blob/master/LICENSE>`_ licence.
It uses a processed version of the ICRP 107 decay data :ref:`[1] <refs>`, which
is originally Copyright |copy| 2008 A. Endo and K.F. Eckerman.

Contributors
------------

* `Alex Malins <https://alexmalins.com>`_

Acknowledgements
----------------

Special thanks to:

* `Center for Computational Science & e-Systems <https://ccse.jaea.go.jp/index_eng.html>`_, `JAEA <https://www.jaea.go.jp/english>`_.
* `Kenny McKee <https://github.com/Rolleroo>`_

for their support and assistance to this project.

.. _refs:

References
----------

1. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_
2. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
3. CR Harris et al. Nat. 585, 357-362 (2020). DOI:`10.1038/s41586-020-2649-2 <https://doi.org/10.1038/s41586-020-2649-2>`_
4. Virtanen et al. Nat. Methods 17, 261-272 (2020). DOI:`10.1038/s41592-019-0686-2 <https://doi.org/10.1038/s41592-019-0686-2>`_
5. PyNE: The Nuclear Engineering Toolkit. `https://pyne.io/ <https://pyne.io/>`_
6. KF Eckerman, AL Sjoreen & C Sun, Radiological Toolbox, Oak Ridge National Laboratory. `https://www.ornl.gov/crpk/software <https://www.ornl.gov/crpk/software>`_
7. B Dahlgren, batemaneq:  a C++ implementation of the Bateman equation, and a Python binding thereof. `https://github.com/bjodah/batemaneq <https://github.com/bjodah/batemaneq>`_
8. A Endo, Y Yamaguchi & KF Eckerman, JAERI 1347 (2005). DOI:`10.11484/jaeri-1347 <https://doi.org/10.11484/jaeri-1347>`_
9. A Endo & KF Eckerman, JAEA-Data/Code 2007-021 (2007). DOI:`10.11484/jaea-data-code-2007-021 <https://doi.org/10.11484/jaea-data-code-2007-021>`_

.. |alpha| unicode:: U+03B1 .. lower case alpha
.. |beta| unicode:: U+03B2 .. lower case beta
.. |epsilon| unicode:: U+03B5 .. lower case epsilon
