# radioactivedecay

radioactivedecay is a Python package for performing radioactive decay calculations. It supports
1252 radionuclides, including full decay chains and branching.

Installation
------------

radioactivedecay requires Python 3.6+, NumPy and SciPy.

radioactivedecay is currently in alpha. Install by cloning or downloading the repository, then

```console
$ cd radioactivedecay
$ pip install -e .
```

Usage
-------

radioactivedecay is based around inventories of radionuclides, which are created as follows

```pycon
>>> import radioactivedecay as rd
>>> tritium_initial = rd.Inventory({'H-3': 10.0})
>>> tritium_initial.contents
{'H-3': 10.0}
```

Here an inventory of 10 Bq of H-3 (tritium) was initialized by supplying a dictionary to
`Inventory()`. Radionuclides can be specified in three equivalent ways:
e.g. 'Rn-222', 'Rn222' or '222Rn'
or 'Ir-192n', 'Ir192n' or '192nIr' (for second metastable state of Ir-192)

Calculate the radioactive decay of an inventory by

```pycon
>>> tritium_decayed = tritium_initial.decay(12.32, 'y')
>>> tritium_decayed.contents
{'H-3': 5.0}
```

In this example the 10 Bq of H-3 was decayed for one half-life (12.32y), yielding 5 Bq of H-3. Note
the `decay()` function takes two arguments: the decay time and its units ('s', 'm', 'h', 'd' or 'y').

The next example is for a mixture of Tc-99m and I-123. It demonstrates the ingrowth of radioactive
progeny via decay chains. The decay period is 20 hours.

```pycon
>>> mix = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
>>> mix.decay(20.0, 'h').contents
{'I-123': 2.040459244534774,
 'Tc-99': 6.729939210983381e-09,
 'Tc-99m': 0.22950748010063513,
 'Te-123': 9.485157551487966e-18}
```

Tc-99 and Te-123 are long half life daughters of Tc-99m and I-123, respectively.

radioactivedecay includes a `Radionuclide` class. It can be used to fetch the half-lives of
radionuclides:

```pycon
>>> rd.Radionuclide('Rn222').halflife('d')
3.8235
```

The half-life of Rn-222 is 3.8235 days.

How it works
--------------

radioactivedecay uses decay data from ICRP Publication 107 (2008).
https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3

It calculates an analytical solution to the decay chain differential equations using matrix algebra.
M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010)
https://doi.org/10.1088/0952-4746/26/3/N02

It is efficient as it uses NumPy and SciPy sparse functions for matrix multiplications.


Limitations
-------------

The following processes are not modelled by radioactivedecay:
- ingrowth of progeny from spontaneous fission decays
- neutronics, so no modelling of induced radioactivity or fission

Care is needed when decaying backwards in time (i.e. supplying a negative time to the decay()
function), as this can result in numerical instabilities and nonsense results.
