# Contributing

Users are welcome to submit bug reports, feature requests, suggestions for
improvements and pull requests for this package. Below are some guidelines
to keep in mind when requesting or making changes.


## Reporting Issues

If you encounter an issue or find a bug in the code, please open an issue on
the GitHub [issues](https://github.com/alexmalins/radioactivedecay/issues)
page.

When submitting issues please include the version of ``radioactivedecay`` and
Python you are using, and include a minimal example of code or information
which demonstrates the problem.


## Making Changes

If you would like to contribute code, bug fixes or documentation to the
project, please fork the GitHub repository, make your changes, then submit a
[pull request](https://github.com/alexmalins/radioactivedecay/pulls).


## Docstrings

Docstrings use the [NumPy format](https://numpydoc.readthedocs.io/en/latest/format.html).
The doctrings are automatically harvested by Sphinx to create the API section
of the [documentation](https://alexmalins.com/radioactivedecay/).


## Release guidelines

To release a new version of ``radioactivedecay``:
* Update version number in setup.py
* Update version number in radioactivedecay/__init__.py
* Update version number in docs/source/conf.py
* Run the tests: ``coverage run -m unittest discover``
* Upload coverage reports to codecov
* Compile docs: ``docs/make html``
* Upload docs to https://alexmalins.com/radioactivedecay/
* Create a release on GitHub
* Upload new version to PyPi
