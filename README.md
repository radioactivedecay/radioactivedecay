# radioactivedecay

[![PyPI](https://img.shields.io/pypi/v/radioactivedecay)](https://pypi.org/project/radioactivedecay/)
[![Python Version](https://img.shields.io/pypi/pyversions/radioactivedecay)](https://pypi.org/project/radioactivedecay/)
[![Latest Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](https://alexmalins.com/radioactivedecay/)
[![Test Coverage](https://codecov.io/gh/alexmalins/radioactivedecay/branch/master/graph/badge.svg)](https://codecov.io/gh/alexmalins/radioactivedecay)

radioactivedecay is a Python package for radioactive decay calculations. It supports full decay
chains, including branching decays and metastable states. By default it uses the ICRP Publication
107 radioactive decay data, which covers 1252 radionuclides.

- **Documentation**: [https://alexmalins.com/radioactivedecay](https://alexmalins.com/radioactivedecay/)

## Installation

radioactivedecay requires Python 3.6+, NumPy and SciPy.

The easiest way to install radioactivedecay is via the [Python Package Index](https://pypi.org/project/radioactivedecay/)
using `pip`:

```console
$ pip install radioactivedecay
```

## Usage

### Example 1
radioactivedecay is based around inventories of radionuclides. These are created as follows:

```pycon
>>> import radioactivedecay as rd
>>> tritium_t0 = rd.Inventory({'H-3': 10.0})
>>> tritium_t0.contents
{'H-3': 10.0}
```

Here we initialized an inventory of 10 Bq of H-3 (tritium) by supplying a Python dictionary to
`Inventory()`. Radionuclides can be specified in three equivalent ways:
* e.g. 'Rn-222', 'Rn222' or '222Rn',
* or 'Ir-192n', 'Ir192n' or '192nIr' (for the second metastable state of Ir-192).

To perform a radioactive decay of an inventory:

```pycon
>>> tritium_t1 = tritium_t0.decay(12.32, 'y')
>>> tritium_t1.contents
{'H-3': 5.0}
```

The 10 Bq of H-3 was decayed for one half-life (12.32 years), yielding 5 Bq of H-3. Note the second
argument to the `decay()` method is the decay time unit. Various units are supported, including 's',
'm', 'h', 'd' and 'y'.

Note also that radioactivedecay does not require specifying activity units. Units out are the same
as units in, so this calculation could have been 10 Ci of H-3 to 5 Ci, or 10 dpm to 5 dpm, 10 kBq
to 5 kBq, etc.

### Example 2
Inventories can contain more than one radionuclide. In this example we start with an inventory that
initially contains Tc-99m and I-123. Decaying this inventory demonstrates the ingrowth of
radioactive progeny via decay chains. For a decay period of 20 hours:

```pycon
>>> mix = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
>>> mix.decay(20.0, 'h').contents
{'I-123': 2.040459244534774,
 'Tc-99': 6.729944738772211e-09,
 'Tc-99m': 0.22950748010063513,
 'Te-123': 9.485166535243877e-18,
 'Te-123m': 7.721174031572363e-07}
```

Tc-99 is the progeny of Tc-99m, and Te-123 and Te-123m are progeny of I-123.

### Example 3
radioactivedecay includes a `Radionuclide` class. It can be used to fetch the half-lives of
radionuclides:

```pycon
>>> rd.Radionuclide('Rn-222').half_life('d')
3.8235
>>> rd.Radionuclide('C-14').half_life('y')
5700.0
```

The half-lives of Rn-222 and C-14 are 3.8235 days and 5700 years, respectively.

## How it works

By default radioactivedecay uses decay data from
[ICRP Publication 107 (2008)](https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3).

It calculates an analytical solution to the decay chain differential equations using matrix and
vector multiplications. It implements the method described in this paper:
[M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010)](https://doi.org/10.1016/j.cpc.2009.08.011).

It calls NumPy and SciPy for the matrix operations.

The notebooks folder in the [GitHub repository](https://github.com/alexmalins/radioactivedecay)
contains some Jupyter Notebooks for creating the
[ICRP 107 decay dataset](https://github.com/alexmalins/radioactivedecay/notebooks/icrp107_dataset)
for radioactivedecay, and cross-checks against
[PyNE](https://github.com/alexmalins/radioactivedecay/notebooks/comparisons/pyne)
and
[Radiological Toolbox](https://github.com/alexmalins/radioactivedecay/notebooks/comparisons/radiological_toolbox_compare.ipynb).

## Limitations

At present radioactivedecay has the following limitations:
- It does not model neutronics, so cannot calculate radioactivity produced from neutron-nuclear
reactions inducing radioactivity or fission.
- It cannot model external sources of radioactivity input to or removal from an inventory over
time.
- radioactivedecay uses double precision floating point numbers for calculations. Numerical
precision issues can arise for decay chains where the half-life of the parent is many orders of
magnitude smaller than the half-life of one of the progeny. Similarly there can be precision issues
when two radionuclides in a chain have very similar (or identical) half-lives. Note that this
latter case does not appear to apply to radionuclides within ICRP 107 dataset, however. If you need
greater numerical precision for your decay calculations, you could investigate using the
[batemaneq](https://pypi.org/project/batemaneq/) package which supports
[arbitrary precision calculations](https://bjodah.github.io/blog/posts/bateman-equation.html).
- Care is needed when decaying backwards in time, i.e. supplying a negative argument to `decay()`,
as this can also result in numerical instabilities and nonsensical results.

There are also some limitations associated with the ICRP 107 decay dataset:
- ICRP 107 does not contain data on branching fractions for radionuclides produced from spontaneous
fission decays. Thus `decay()` calls do not calculate the spontaneous fission progeny.
- Decay data is quoted in ICRP 107 with up to 5 significant figures of precision. The results of
decay calculations will therefore not be more precise than this level of precision.
- Uncertainties are not quoted for the radioactive decay data in ICRP 107. Uncertainties will vary
substantially between radionuclides, e.g. depending on how well each radionuclide has been
researched in the past. In many cases these uncertainties more significant for the results of
decay calculations than the previous point about the quoted precision of the ICRP 107 decay data.
- There are a few instances where minor decay pathways were not included in ICRP 107. Examples
include the decays At-219-> Rn-219 (&beta; ~3%), Es-250 -> Bk-246 (&alpha; ~1.5%), and
U-228 -> Pa-228 (&epsilon; ~2.5%). For more details see the following references on the creation of
the ICRP 107 dataset: [JAERI 1347](https://doi.org/10.11484/jaeri-1347) &
[JAEA-Data/Code 2007-021](https://doi.org/10.11484/jaea-data-code-2007-021).

## Acknowledgements

Special thanks to
* [Center for Computational Science & e-Systems](https://ccse.jaea.go.jp/index_eng.html),
Japan Atomic Energy Agency
* [Kenny McKee](https://github.com/Rolleroo)

for their help and support to this project.
