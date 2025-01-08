# Changelog

## [0.6.0] - 2025-01-08
- Modernize build system using a single `pyproject.toml` (#115).
- Drop Python 3.8 support and add Python 3.13 support (#115).
- Code quality improvements: PEP 585 style type hints, some mypy, black & pylint fixes, and
increased test coverage (#115).
- Fix test failures with Sympy >=1.13.2 (#109).

## [0.5.1] - 2024-06-18
- Fix tests to work with NumPy 2.0.0 NEP 51 string representations of NumPy data types (#107).

## [0.5.0] - 2024-04-20
- Add `Inventory.decay_time_series_pandas()` method to save decay data into a pandas dataframe. Time
resolution is specified by the user (#104).
- Add `Inventory.decay_time_series()` method to access the decay data create by `decay_time_series_pandas()`
as a list for the time data and dictionary for the isotopic data (#104).
- Drop support for end-of-life Python versions v3.6 & v3.7 (#106).
- Fix `pkg_resources` deprecation warnings and some pylint warnings (#106).

## [0.4.22] - 2024-01-27
- Added explicit support for Python v3.12. 

## [0.4.21] - 2023-08-13
- Add `Inventory.to_csv()` and `InventoryHP.to_csv()` methods for writing an inventory's contents
to a CSV file (in user's chosen units) (#94).

## [0.4.20] - 2023-08-08
- Add `rd.read_csv()` function for creating an inventory by reading nuclides & quantities (and
optionally units) in from a CSV file (#94).

## [0.4.19] - 2023-08-05
-  Fix bug whereby inventories would not instantiate with NumPy int datatypes (e.g. `numpy.int32`)
for the nuclide quantity in the instantiation dictionary. Previously a ValueError was raised (#96).

## [0.4.18] - 2023-06-27
-  Prohibit instantiation of an inventory if the user supplies an activity for a stable nuclide
(#92).

## [0.4.17] - 2023-03-10
- Fix bug where the conversion of dpm to other activity units, and vice versa, was incorrect (#87 &
#88).

## [0.4.16] - 2022-10-29
- Added support for Python v3.11. Use latest importlib-resources API (`files()` etc.) to fix
warnings. Fix pylint `__repr__()` usage warnings in tests. Use isort to sort imports and check in
code formatting action (#85).

## [0.4.15] - 2022-09-08
- Fix normal precision inventory unit tests for `decay()` and `cumulative_decays()` methods (#84).
The tests now warn if the calculated floats are not exact matches for the test defaults, and assert
that the calculated floats are within max(rel_tol=1e-7, abs_tol=1e-30) of the expected values. This
means the tests that had previously started flaking on GitHub Actions CI (sporadically) will now
pass.

## [0.4.14] - 2022-09-06
- Fix bug where high-precision (SymPy) default dataset had incorrect half-lives for Th-232, Sm-147
and Rb-87 (#82). All users performing `InventoryHP` decay calculations for chains containing these
radionuclide are encouraged to upgrade without delay. Previous radioactivedecay versions gave
incorrect results (note normal precision `Inventory` decays were unaffected).

## [0.4.13] - 2022-05-17
- Code improvement to support metastable states up to 6th state (#76).
- Added labels for more decay modes (including heavy cluster decay modes) to decay chain plots code
(#77).
- Improve parsing of nuclide strings (#78). Note: you must use the correct capitalization of the
metastable state and the element chars when using mass number first format, e.g. use '130nI' to get
I-130n, not '130ni', '130Ni' or '130NI' as these will be mistaken as Nickel (Ni). Capitalization
does not matter if using element first formats, e.g. 'I-130N' or 'I130N' will be correctly parsed
to I-130n.

## [0.4.12] - 2022-3-24
- Added more stable products to the default ICRP-107 dataset (#75).

## [0.4.11] - 2022-03-20
- Default `ymin` for Inventory `plot()` method is now 0.95x the minimum quantity that occurs over
the decay period when `yscale='log'` (#70 & #72).
- Improved nuclide string parsing: robust to nuclide strings containing whitespaces and some
incorrect capitalizations of the element / metastable state chars (#65 & #72).
- Fix `load_dataset()` docstring not showing in decaydata API docpage (#71).

## [0.4.10] - 2022-03-15
- Fix incorrect parsing of SymPy version string (#67, #68). This bug meant radioactivedecay import
failed if using SymPy >=1.10. The fix makes Setuptools an explicit dependency.

## [0.4.9] - 2022-02-07
- Code refactoring: reduce coupling between modules by refactoring Converter, Nuclide & Inventory
classes to not store duplicate data, but to receive data when needed via their API calls. DecayData objects
no longer store Converter objects. Continuing to reduce pylint/mypy errors/warnings, however will
need to wait to bump requirement to Python 3.7+ to improve type hinting of NumPy/SciPy arrays
(requires NumPy 1.20+, holding off for now to maintain Python 3.6 support) (#64, #66).
- Improve API documentation table of contents & README fix (#66).
- Better unit tests for DecayData class and error handling is instance does not contain SymPy data
(#66).
- Move dataset creation and comparison notebooks to separate repos within the radioactivedecay org
on GitHub (#63).
- Tweak GitHub Issue & PR markdown templates (#62).

## [0.4.8] - 2021-12-13
- Fix some code bugs and make other improvements to the ReadMe and the Docs (#57, #58 & #59).
- Reduce number of mypy errors, use Python f-strings everywhere (#60).
- Fix the URL for the codecov badge in the ReadMe (#56 & #60).
- Introduce GitHub Actions for CI/CD. Add Issue & Pull Request templates (#61).

## [0.4.7] - 2021-11-08
- Fix old references to `Radionuclide` class in Readme, docs and docstrings (#54 & #55). This class
was renamed to `Nuclide` from release v0.4.0.
- Other small rewrites to docs.

## [0.4.6] - 2021-10-21
- Projected transferred into radioactivedecay organization on GitHub: updated code & docs
accordingly.
- Moved hosting of docs to GitHub Pages (https://radioactivedecay.github.io).
- Opened forum for project at https://github.com/radioactivedecay/radioactivedecay/discussions
(uses GitHub Discussions).
- Only store radioactivedecay version number in radioactivedecay/__init__.py file. Read this file
to obtain version number in setup.py and docs/source/conf.py.

## [0.4.5] - 2021-10-15
- Latest SymPy release (v1.9) changed internals of Rational / Matrix objects. This breaks loading
of SymPy <=1.8 pickle objects when using SymPy v1.9. `radioactivedecay` now packages SymPy pickle
files appropriate for SymPy <=1.8 and for SymPy >=1.9. It checks which SymPy version is in the
local environment before choosing the correct files to load (fixes issue #50 and failure of
`radioactivedecay` v0.4.4 to build on the conda-forge feedstock).
- Added support for Python v3.10 (PyPI only, not yet available via conda-forge).
- Move responsibility for file I/O from `DecayData` class initiator into separate function called
`load_dataset()`.

## [0.4.4] - 2021-10-08
- Fix docstring typo, Inventory `plot()` method (#48).

## [0.4.3] - 2021-10-01
- Refactored DecayData class to store progeny, branching fractions and decay modes data in
separate numpy arrays.
- Use np.array_equal() for checking equality of numpy arrays.
- Fix bug which caused scipy C and C^-1 matrices to be unnecessarily large.
- Added tests to check shape of scipy C and C^-1 matrices from icrp107_ame2020_nubase2020 dataset.
- Use idx as variable name for index of for loops.

## [0.4.2] - 2021-09-15
- Fixed bug in `InventoryHP` meaning `decay()` gave some incorrect results.
- Hard-coded Avogadro's constant to avoid tests failing with older versions of SciPy.
- Updated notebooks to be consistent with v0.4.0+.

## [0.4.1] - 2021-09-07
- Added ICRP-07 and AMDC license files into MANIFEST.in. Includes these files in PyPI package.

## [0.4.0] - 2021-09-06
- Release 0.4.0 is a large update to `radioactivedecay`. It adds functionality to supply nuclide
masses, moles and numbers of atoms when creating inventories, and also methods so inventories can
report their contents in terms of these quantities, as well as mass or atom fractions (#35). Mass
conversions use atomic mass data from the Atomic Mass Data Center (AMDC) by default.
- To enable SymPy high precision calculations throughout unit and quantity conversions, there is a
new `InventoryHP` class (high-precision inventory class). This behaves the same as the normal
precision `Inventory` class. The old `Inventory.decay_high_precision()` method is now deprecated -
use `InventoryHP.decay()` instead for high-precision decay calculations.
The number of significant figures for high precision decay calculations is now specified via the
`InventoryHP.sig_fig` attribute (default is 320) rather than as a parameter to the `InventoryHP`
`decay()` and `plot()` methods.
- Added new `cumulative_decays()` method to the inventory classes. This calculates the total number
of atoms of each radionuclide that decay over the decay time period.
- Added support to specify nuclides using canonical ids (#36).
- Documentation updates for all new and modified functionality.
- LICENSE file split into separate files for `radioactivedecay`, ICRP-107 decay data, and AMDC
atomic mass data (#38).
- Added parsing of AME2020 and NuBase2020 atomic mass and isomer excitation energy data to ICRP-107
dataset Jupyter notebook. Added stable nuclides to decaydata.npz file, C and C_inv matrix SciPy
and SymPy files in ICRP-107 (#33 & #34).

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
