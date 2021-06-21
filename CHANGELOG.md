# Changelog

## [0.3.4] - 2021-06-21
- Fix bug in decay chain plots which caused overlaps of some radionuclides in complicated chains.
- Document method for installing via conda.
- Improve clarity of matplotlib imports.
- Correct a DecayData attribute docstring entry.

## [0.3.3] - 2021-05-14
- Improve readme and fix typo.
- Add MANIFEST.in so LICENSE and markdown files get packaged.
- Update year in LICENSE file.

## [0.3.2] - 2021-04-14
- Allow specification of `sig_fig` as a parameter to the `decay_high_precision()` method.
- Improve code with respect to pylint and mypy checks.
- Add discussion on the radioactive progeny that are not in the ICRP-107 data to the limitations
section of the docs and to the Jupyter notebook analyzing the ICRP-107 data.
- Update other Jupyter notebooks for this release.
- Theory docpage typo fix.

## [0.3.1] - 2021-04-07
- Fix bugs upon supplying Matplotlib Figure or Axes objects to `Inventory` and `Radionuclide`
`plot()` methods.
- Docs and ReadMe updates.
- Changelog typo fixes.

## [0.3.0] - 2021-03-31
- Add `plot()` method to `Radionuclide` class for creating decay chain diagrams. This adds a
dependency on the NetworkX library.
- Changes to `plot()` method of `Inventory` class: fix for bug which ignored the user setting of
`npoints` when using high precision decay mode, docstring fixes, no longer call `plt.show()`.
- Mistakes in comments of unittest python files.

## [0.2.4] - 2021-03-20
- Add `Inventory.half_life()` method as spelling variation of `Inventory.half_lives()`
- ReadMe: simplify. Use `'readable'` for inv_t1 half-lives example.

## [0.2.3] - 2021-03-15
- Improve `'readable'` half-life strings for radionuclides with half-lives less than 1 s or
greater than 1000 years.
- Switch from reporting microseconds as `'us'` to `'μs'`.
- Docs improvements: required packages and acknowledgements.
- ReadMe: Matplotlib dependency is used for plotting.
- Changelog typo fixes.

## [0.2.2] - 2021-03-08
- Supply `'readable'` as time unit parameter to half-life methods to get strings with the
half-lives in human-readable units.
- Add support for unicode `'μs'` and for `'By'` (billion year) time units.
- Changed the `Inventory.plot()` graphs so that the decay curves are ordered from highest to lowest
radionuclides in the decay chains by default. Alphabetical ordering can be specified by supplying
the new `order=='alphabetical'` parameter to the method.
- `DecayData.half_life()` method docstring typo fix.

## [0.2.1] - 2021-01-26
- Fixed version numbers.
- Updated logo.
- Use logo hosted on GitHub in ReadMe.

## [0.2.0] - 2021-01-22
- Adds plot() method for creating inventory decay graphs using matplotlib.
- New logo in readme and docs.

## [0.1.1] - 2021-01-07
- Documentation improvements, including improved theory docpage on numerical
computation methods.

## [0.1.0] - 2020-12-02
- Adds `decay_high_precision()` method for high numerical precision decay
calculations (adds a new dependency on the SymPy package).
- Code refactoring. Decay dataset format overhauled.
- ReadMe and Docs updates.

## [0.0.9] - 2020-11-24
- Add support for using `Radionuclide` objects in place of radionuclide strings for `Inventory`
constructor, `add()` and `remove()` methods.
- Add `Radionuclide` `__hash__()` method (needed for above change).
- Add `half_lives()`, `progeny()`, `branching_fractions()` and `decay_modes()` methods to
`Inventory`.
- Add type hinting.
- Add support for calling `len()` on an `Inventory` to find the number of radionuclides it
contains.
- Add support for `==` and `!=` operators with `DecayData`, `Radionuclide` and `Inventory`
instances.
- Add support for `'ps'` (picoseconds) time unit.
- Code refactoring. `Radionuclide` and `Inventory` classes moved into separate files.
- In icrp107_dataset.ipynb, clarify that ICRP-107 does not contain data on spontaneous fission
outcomes.
- ReadMe and Docs updates (mainly updates of the theory and tutorial docpages).

## [0.0.8] - 2020-10-13
- Add methods to `Radionuclide` class for fetching branching fractions and decay modes.
- Add methods to `DecayData` class for fetching half-lives, branching fractions and decay modes.
- Refactor utility functions into their own .py source file.
- Fix broken links to notebooks.
- ReadMe and Docs updates.
- Add code of conduct and contributing guidelines.

## [0.0.7] - 2020-10-06
- Restore notebooks folder.
- Add comparison to Radiological Toolbox v3.0.0.
- Add comparison to PyNE v0.7.2.
- Use Black for code formatting.
- ReadMe and Docs updates.
- Add theory section to docs.
- Fix bug in loading custom decay dataset files (allow_pickle=True in np.load()).
- Restore support for Python 3.9.

## [0.0.6] - 2020-08-30
- Create docs ([https://alexmalins.com/radioactivedecay](https://alexmalins.com/radioactivedecay/)).
- Add NumPy style docstrings to code.
- Add unit tests and code coverage.
- Add option to read in own decay datafiles into a `DecayData` object.
- Add day to year conversion factor as an instance variable of `DecayData` objects.
- Switch day to year conversion used with ICRP 107 dataset to 365.2422 days per year to be
consistent with how ICRP 107 was originally made (this also required updating the
ICRP 107 datafiles created for radioactivedecay).
- Add support for 'ns' (nanosecond) time unit.
- Add operators for multiplication and division of `Inventory` objects (acts on radionuclide
activities).
- Optimize `decay()` method for faster calculations.
- Refactor loading of packaged decay data files in decaydata.py.
- Refactor functions in decayfunctions.py to only take necessary data as arguments.
- Remove Python 3.9 from setup.py as it is not officially released yet.
- Update and improve the ReadMe.

## [0.0.5] - 2020-07-16
- New support for `Inventory` object arithmetic (addition and subtract of `Inventory` objects).
- New methods for adding, subtracting and removing from `Inventory` objects.
- Added support for more time units ('us' for microseconds, 'ms' for milliseconds, 'ky' for
kiloyears, 'My' for megayears, 'Gy' for gigayears, 'Ty' for terayears and 'Py': for petayears).
Also add support for some other strings for seconds ('sec', 'second', 'seconds'), hours ('hr',
'hour', 'hours'), days ('day', 'days') and years ('yr', 'year', 'years').
- Add new descriptive printable representations for objects.
- Convert `Inventory` radionuclides and activities instance variables to property.
- Associate decay dataset with Radionuclide() objects.
- Improve readme.
- Move Jupyter Notebooks to separate git repository.
(https://github.com/alexmalins/radioactivedecay-notebooks)

## [0.0.4] - 2020-06-13
- Fix bugs affecting missing decay modes for some radionuclides.
- Add Jupyter Notebook for generating the ICRP 107 decay dataset files.
- Add Jupyter Notebook to test functionality and check results against a baseline version.

## [0.0.3] - 2020-06-02
- Fix bugs affecting parsing of arguments.

## [0.0.2] - 2020-06-02
- Add PyPI support.
- Fix bug in validity check of dictionary argument to `Inventory` affecting Python 3.8+.

## [0.0.1] - 2020-06-02
- First alpha release of radioactivedecay package.