# Changelog

## [0.0.5] - 2020-07-16
- New support for Inventory() arithmetic (addition and subtract of Inventory() objects).
- New methods for adding, subtracting and removing from Inventory() objects.
- Added support for more time units ('us' for microseconds, 'ms' for milliseconds, 'ky' for
kiloyears, 'My' for megayears, 'Gy' for gigayears, 'Ty' for terayears and 'Py': for petayears).
Also add support for some other strings for seconds ('sec', 'second', 'seconds'), hours ('hr',
'hour', 'hours'), days ('day', 'days') and years ('yr', 'year', 'years').
- Add new descriptive printable representations for objects.
- Convert Inventory() radionuclides and activities instance variables to property.
- Associate decay dataset with Radionuclide() objects.
- Improve readme.
- Move Jupyter Notebooks to separate git repository.
(https://github.com/alexmalins/radioactivedecay-notebooks)

## [0.0.4] - 2020-06-13
- Fix bugs affecting missing decay modes for some radionuclides.
- Add Jupyter Notebook for generating the ICRP-07 dataset files.
- Add Jupyter Notebook to test functionality and check results against a baseline version.

## [0.0.3] - 2020-06-02
- Fix bugs affecting parsing of arguments.

## [0.0.2] - 2020-06-02
- Add PyPI support.
- Fix bug in validity check of dictionary argument to Inventory() affecting Python 3.8+.

## [0.0.1] - 2020-06-02
- First release of radioactivedecay package.