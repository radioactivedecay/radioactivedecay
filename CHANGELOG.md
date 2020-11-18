# Changelog

## [0.0.9] - XXX
- Add support for calling `len()` on an inventory to find the number of radionuclides it contains.
- Add type hinting.
- Code refactoring.
- In icrp107_dataset.ipynb, clarify that ICRP-107 does not contain data on spontaneous fission outcomes.
- ReadMe and Docs updates (large update of the theory docpage).

## [0.0.8] - 2020-10-13
- Add methods to `Radionuclide` class for fetching branching fractions and decay modes.
- Add methods to `DecayData` class for fetching half-lives, branching fractions and decay modes.
- Refactor utility functions into their own .py source file.
- Fix broken links to notebooks.
- ReadMe and Docs updates.
- Add code of conduct and contributing guidelines.

## [0.0.7] - 2020-10-06
- Restore notebooks folder.
- Add comparison to Radiological Tookbox v3.0.0.
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
- Add opetators for multpication and division of `Inventory` objects (acts on radionuclide
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