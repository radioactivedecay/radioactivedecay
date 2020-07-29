Installing radioactivedecay
===========================

Prerequisites
-------------

``radioactivedecay`` requires a Python 3.6+ installation with the `NumPy
<https://numpy.org/>`_ and `SciPy <https://www.scipy.org/index.html>`_
packages. These can be installed from `python.org <https://www.python.org/>`_
and `PyPI <https://pypi.org/>`_, or via a package manager such as `Anaconda
<https://www.anaconda.com/>`_, `WinPython <https://winpython.github.io/>`_,
`MacPorts <https://www.macports.org/>`_, `HomeBrew <https://brew.sh/>`_,
`APT <https://en.wikipedia.org/wiki/APT_(software)>`_ etc.

Installation
------------

The easiest way to install ``radioactivedecay`` is via the `Python Package
Index <https://pypi.org/>`_ using ``pip``:

.. code-block:: bash

    pip install radioactivedecay

This will also try to install NumPy and SciPy if they are not already present
in the Python environment.

You can also clone or download the repository from `GitHub
<https://github.com/alexmalins/radioactivedecay>`_ and then from inside the
``radioactivedecay`` folder install via the command:

.. code-block:: bash

    pip install -e .
    