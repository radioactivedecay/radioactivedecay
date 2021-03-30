Overview
========

Introduction
------------

``radioactivedecay`` is a Python package for radioactive decay calculations.
It contains functions to define inventories of radionuclides, perform
decay calculations, and output decay data for radionuclides and decay chains.

The original goal was to create a light-weight Python package for radioactive
decay calculations, with full support for branching decays, multi-step decay
chains, and metastable states. ``radioactivedecay`` uses the decay data from
ICRP Publication 107 :ref:`[1] <refs>` by default. It solves the radioactive
decay differential equations analytically using basic linear algebra operations
:ref:`[2] <refs>`.

In order to use ``radioactivedecay``, you will need Python 3.6+ with the
Matplotlib, NumPy, SciPy, and SymPy packages installed. The code is platform
independent and has been tested on Windows, MacOS and Linux systems.

Quick Start
-----------

Install ``radioactivedecay`` via the command:

.. code-block:: bash

    $ pip install radioactivedecay
    
This command will also attempt to install Matplotlib, NumPy, SciPy and SymPy
if they are not already present in your environment.

Import the ``radioactivedecay`` package and decay a simple inventory using:

.. code-block:: python3

    >>> import radioactivedecay as rd
    >>> inv_t0 = rd.Inventory({'H-3': 10.0})
    >>> inv_t1 = inv_t0.decay(12.32, 'y')
    >>> inv_t1.contents
    {'H-3': 5.0}

Here we created an inventory of 10.0 units of tritium (:sup:`3`\H) and decayed
it for 12.32 years. The activity reduced by a factor of two, i.e. to 5.0 units,
as 12.32 years is the half-life of tritium.

``radioactivedecay`` is agnostic to activity units: the output units are the
same as the input units. The above example could therefore represent 10.0 Bq of
tritium decaying to 5.0 Bq, or 10.0 Ci to 5.0 Ci, or whichever activity unit
you prefer.

Use the ``plot()`` method to show the decay of the inventory over time:

.. code-block:: python3

    >>> inv_t0.plot(100, 'y')

.. image:: images/H-3_decay.png
  :width: 450

The graph shows the decay of H-3 over a 100 year period.

Use the ``Radionuclide`` class to fetch decay data about a particular
radionuclide and to draw diagrams of its decay chain:

.. code-block:: python3

    >>> nuc = rd.Radionuclide('H-3')
    >>> nuc.half_life('readable')
    '12.32 y'
    >>> nuc.progeny()
    ['He-3']
    >>> nuc.decay_modes()
    ['β-']
    >>> nuc.branching_fractions()
    [1.0]
    >>> nuc.plot()

.. image:: images/H-3_chain.png
  :width: 100

How it works
------------

``radioactivedecay`` calculates an analytical solution to the decay chain
differential equations using matrix and vector multiplications. It implements
the method described in ref. :ref:`[2] <refs>`.  See the
`theory docpage <https://alexmalins.com/radioactivedecay/theory.html>`_ for
more details. It calls NumPy :ref:`[3] <refs>` and SciPy :ref:`[4] <refs>` for
the matrix operations. There is also a high numerical precision decay
calculation mode based on SymPy :ref:`[5] <refs>` routines.

The `notebooks folder 
<https://github.com/alexmalins/radioactivedecay/tree/main/notebooks>`_ 
in the GitHub repository contains some Jupyter Notebooks for creating the 
`ICRP-107 decay dataset
<https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/icrp107_dataset/icrp107_dataset.ipynb>`_
for ``radioactivedecay``, and cross-checks against `PyNE
<https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/comparisons/pyne/rd_pyne_truncated_compare.ipynb>`_ 
:ref:`[6] <refs>` and `Radiological Toolbox 
<https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/comparisons/radiological_toolbox/radiological_toolbox_compare.ipynb>`_
:ref:`[7] <refs>`.

Limitations
-----------

At present ``radioactivedecay`` has the following limitations:

* It does not model neutronics, so cannot calculate radioactivity produced
  from neutron-nuclear reactions inducing radioactivity or fission.
* It cannot model temporal sources of external radioactivity input or removal
  from an inventory over time.
* Care is needed when decaying backwards in time, i.e. supplying a negative
  argument to the ``decay()`` and ``decay_high_precision()`` methods, as this
  can result in numerical instabilities and nonsensical results.

There are also some limitations associated with the ICRP-107 decay dataset:

* ICRP-107 does not contain data on branching fractions for radionuclides
  produced from spontaneous fission decays. Thus ``decay()`` and
  ``decay_high_precision()`` do not calculate activities for spontaneous
  fission progeny.
* Decay data is quoted in ICRP-107 with up to 5 significant figures of
  precision. The results of decay calculations will therefore in theory never
  be more precise than this level of precision.
* Uncertainties are not quoted for the radioactive decay data in ICRP-107.
  Uncertainties will vary substantially between radionuclides. They will depend
  on how well each radionuclide has been researched in the past. In many cases
  these uncertainties will be more significant for the results of decay
  calculations than the previous point about the quoted precision of the
  ICRP-107 decay data.
* There are a few instances where minor decay pathways were not included in
  ICRP-107, e.g. the decay pathways for At-219-> Rn-219 (|beta| ~3%), Es-250 ->
  Bk-246 (|alpha| ~1.5%), and U-228 -> Pa-228 (|epsilon| ~2.5%). For more
  details see refs. :ref:`[8] <refs>` and :ref:`[9] <refs>` on the creation of
  the ICRP-107 dataset.

License
-------

.. include:: <isonum.txt>

``radioactivedecay`` is open source software released under the `MIT 
<https://github.com/alexmalins/radioactivedecay/blob/master/LICENSE>`_ licence.
It uses a processed version of the ICRP-107 decay data :ref:`[1] <refs>`, which
is originally Copyright |copy| 2008 A. Endo and K.F. Eckerman.

Contributors & Contributing
---------------------------

* `Alex Malins <https://alexmalins.com>`_

Users are welcome to fix bugs, add new features or make feature requests.
Please open a pull request or a new issue on the
`GitHub repository <https://github.com/alexmalins/radioactivedecay>`_.

Acknowledgements
----------------

Special thanks to:

* `Center for Computational Science & e-Systems <https://ccse.jaea.go.jp/index_eng.html>`_, JAEA.
* `Kenny McKee <https://github.com/Rolleroo>`_
* `Daniel Jewell <https://github.com/danieldjewell>`_

for their support and assistance to this project.

Thanks also to:

* `Björn Dahlgren <https://github.com/bjodah>`_ (author of the batemaneq
  Python package :ref:`[10] <refs>`)
* `Anthony Scopatz <https://github.com/scopatz>`_ and the PyNE project
  :ref:`[6] <refs>`
* `Jonathan Morrell <https://github.com/jtmorrell>`_ (author of the `NPAT
  <https://github.com/jtmorrell/npat>`_ and `Curie
  <https://github.com/jtmorrell/npat>`_ packages)

for their work on open source radioactive decay calculation software.

.. _refs:

References
----------

1. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_
2. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
3. CR Harris et al. Nat. 585, 357-362 (2020). DOI: `10.1038/s41586-020-2649-2 <https://doi.org/10.1038/s41586-020-2649-2>`_
4. P Virtanen et al. Nat. Methods 17, 261-272 (2020). DOI: `10.1038/s41592-019-0686-2 <https://doi.org/10.1038/s41592-019-0686-2>`_
5. A Meurer et al. PeerJ Comp. Sci. 3, e103 (2017). DOI: `10.7717/peerj-cs.103 <https://doi.org/10.7717/peerj-cs.103>`_
6. PyNE: The Nuclear Engineering Toolkit. `https://pyne.io/ <https://pyne.io/>`_
7. KF Eckerman, AL Sjoreen & C Sun, Radiological Toolbox, Oak Ridge National Laboratory. `https://www.ornl.gov/crpk/software <https://www.ornl.gov/crpk/software>`_
8. A Endo, Y Yamaguchi & KF Eckerman, JAERI 1347 (2005). DOI: `10.11484/jaeri-1347 <https://doi.org/10.11484/jaeri-1347>`_
9. A Endo & KF Eckerman, JAEA-Data/Code 2007-021 (2007). DOI: `10.11484/jaea-data-code-2007-021 <https://doi.org/10.11484/jaea-data-code-2007-021>`_
10. B Dahlgren, batemaneq:  a C++ implementation of the Bateman equation, and a Python binding thereof. `https://github.com/bjodah/batemaneq <https://github.com/bjodah/batemaneq>`_

.. |alpha| unicode:: U+03B1 .. lower case alpha
.. |beta| unicode:: U+03B2 .. lower case beta
.. |epsilon| unicode:: U+03B5 .. lower case epsilon
