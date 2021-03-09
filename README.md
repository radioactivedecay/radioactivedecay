[![PyPI](https://img.shields.io/pypi/v/radioactivedecay)](https://pypi.org/project/radioactivedecay/)
[![Python Version](https://img.shields.io/pypi/pyversions/radioactivedecay)](https://pypi.org/project/radioactivedecay/)
[![Latest Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](https://alexmalins.com/radioactivedecay/)
[![Test Coverage](https://codecov.io/gh/alexmalins/radioactivedecay/branch/master/graph/badge.svg)](https://codecov.io/gh/alexmalins/radioactivedecay)

<img src="https://raw.githubusercontent.com/alexmalins/radioactivedecay/main/docs/source/images/radioactivedecay.png" alt="radioactivedecay logo" width="500"/>

``radioactivedecay`` is a Python package for radioactive decay calculations.
It supports decay chains of radionuclides, metastable states and branching
decays. By default it uses the decay data from ICRP Publication 107, which
contains 1252 radionuclides of 97 elements.

It solves the radioactive decay differential equations analytically using NumPy
and SciPy linear algebra routines. There is also a high numerical precision
mode using SymPy routines which gives more accurate results for decay chains
with orders of magnitude differences between radionuclide half-lives.

- **Full Documentation**: 
[https://alexmalins.com/radioactivedecay](https://alexmalins.com/radioactivedecay/)


## Installation

``radioactivedecay`` requires Python 3.6+, NumPy and SciPy.

The easiest way to install ``radioactivedecay`` is via the
[Python Package Index](https://pypi.org/project/radioactivedecay/) using
``pip``:

```console
$ pip install radioactivedecay
```


## Usage

### Decay calculations

Create an ``Inventory`` of radionuclides and decay it as follows:

```pycon
>>> import radioactivedecay as rd
>>> inv_t0 = rd.Inventory({'Mo-99': 2.0})
>>> inv_t1 = inv_t0.decay(20.0, 'h')
>>> inv_t1.contents
{'Mo-99': 1.6207863893776937,
'Tc-99': 9.05304236308454e-09,
'Tc-99m': 1.3719829376710406}
```

Here we created an ``Inventory`` of 2.0 Bq of Mo-99 and decayed it for 20
hours. The decayed ``Inventory`` contains Tc-99m and Tc-99, which are the
progeny of Mo-99.

Note the ``Inventory`` constructor did not require specification of activity
units. This is because in ``radioactivedecay``, units out are the same as units
in, by default. So the above calculation could have represented the decay of 2.0
 Ci of Mo-99, or 2.0 dpm, or 2.0 kBq, etc.

In the example we supplied ``'h'`` as an argument to the ``decay()`` method to
specify the decay time period (20.0) had a time unit of hours. Acceptable time
units for the program include ``'ms'``, ``'s'``, ``'m'``, ``'h'``, ``'d'``,
``'y'`` etc. Note seconds (``'s'``) is the default if no time unit is supplied
to ``decay()``.

Radionuclides can be specified in three equivalent ways in
``radioactivedecay``. The strings

* ``'Rn-222'``, ``'Rn222'`` or ``'222Rn'``,
* ``'Ir-192n'``, ``'Ir192n'`` or ``'192nIr'``

are all equivalent ways of specifying <sup>222</sup>Rn and <sup>192n</sup>Ir to
the program.


### Plotting decay graphs

Use the ``plot()`` method to create graphs of the radioactive decay of an
``Inventory`` over time:

```pycon
>>> inv_t0.plot(20, 'd')
```

<img src="https://alexmalins.com/radioactivedecay/Mo-99_decay.png" alt="Mo-99 decay graph" width="450"/>

This shows the decay of Mo-99 over 20 days, resulting in the ingrowth of Tc-99m
and a trace amount of Tc-99. Plots are drawn using Matplotlib.


### Fetching decay data

``radioactivedecay`` includes methods to fetch decay data for the radionuclides
in an ``Inventory``:

```pycon
>>> inv_t1.half_lives('d')
{'Mo-99': 2.7475, 'Tc-99': 77102628.42, 'Tc-99m': 0.250625}
>>> inv_t1.progeny()
{'Mo-99': ['Tc-99m', 'Tc-99'], 'Tc-99': ['Ru-99'], 'Tc-99m': ['Tc-99', 'Ru-99']}
>>> inv_t1.branching_fractions()
{'Mo-99': [0.8773, 0.1227], 'Tc-99': [1.0], 'Tc-99m': [0.99996, 3.7e-05]}
>>> inv_t1.decay_modes()
{'Mo-99': ['β-', 'β-'], 'Tc-99': ['β-'], 'Tc-99m': ['IT', 'β-']}
```

The ``Radionuclide`` class can be used to fetch decay information for
individual radionuclides, e.g. for Rn-222:

```pycon
>>> nuc = rd.Radionuclide('Rn-222')
>>> nuc.half_life('d')
3.8235
>>> nuc.progeny()
['Po-218']
>>> nuc.branching_fractions()
[1.0]
>>> nuc.decay_modes()
['α']
```


### High numerical precision decay calculations

``radioactivedecay`` includes a high numerical precision mode which gives more
accurate results for decay chains containing long and short lived radionuclides
together. It employs SymPy arbitrary-precision numerical routines. Access it
with the ``decay_high_precision()`` method:

```pycon
>>> inv_t0 = rd.Inventory({'U-238': 1.0})
>>> inv_t1 = inv_t0.decay_high_precision(10.0, 'd')
>>> inv_t1.contents
{'At-218': 1.4511675857141352e-25,
'Bi-210': 1.8093327888942224e-26,
'Bi-214': 7.09819414496093e-22,
'Hg-206': 1.9873081129046843e-33,
'Pa-234': 0.00038581180879502017,
'Pa-234m': 0.24992285949158477,
'Pb-210': 1.0508864357335218e-25,
'Pb-214': 7.163682655782086e-22,
'Po-210': 1.171277829871092e-28,
'Po-214': 7.096704966148592e-22,
'Po-218': 7.255923469955255e-22,
'Ra-226': 2.6127168262000313e-21,
'Rn-218': 1.4511671865210924e-28,
'Rn-222': 7.266530698712501e-22,
'Th-230': 8.690585458641225e-16,
'Th-234': 0.2499481473619856,
'Tl-206': 2.579902288672889e-32,
'Tl-210': 1.4897029111914831e-25,
'U-234': 1.0119788393651999e-08,
'U-238': 0.9999999999957525}
```

## How radioactivedecay works

``radioactivedecay`` calculates an analytical solution to the radioactive decay
differential equations using linear algebra operations. It implements the
method described in this paper:
[M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23
(2010)](https://doi.org/10.1016/j.cpc.2009.08.011). See the
[theory docpage](https://alexmalins.com/radioactivedecay/theory.html) for more
details.

It uses NumPy and SciPy routines for standard double-precision floating-point
computations, and SymPy for high numerical precision calculations.

By default ``radioactivedecay`` uses decay data from
[ICRP Publication 107
(2008)](https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3).

The [notebooks
folder](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks)
in the GitHub repository contains Jupyter Notebooks for creating the decay
datasets that are read in by ``radioactivedecay``, e.g.
[ICRP
107](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/icrp107_dataset/icrp107_dataset.ipynb).
It also contains some comparisons against decay calculations made with
[PyNE](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/comparisons/pyne/rd_pyne_truncated_compare.ipynb)
and
[Radiological
Toolbox](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/comparisons/radiological_toolbox/radiological_toolbox_compare.ipynb).


## Tests

From the base directory run:

```console
$ python -m unittest discover
```


## License

``radioactivedecay`` is open source software released under the MIT License. The
ICRP-107 decay data is copyright 2008 A. Endo and K.F. Eckerman. See
[LICENSE](https://github.com/alexmalins/radioactivedecay/blob/main/LICENSE) for
details. 


## Contributing

Contributors are welcome to fix bugs, add new features or make feature 
requests. Please open a pull request or a new issue on the
[GitHub repository](https://github.com/alexmalins/radioactivedecay).

