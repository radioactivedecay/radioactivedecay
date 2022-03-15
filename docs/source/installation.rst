Installation
============

Prerequisites
-------------

``radioactivedecay`` requires Python 3.6+ and the `Matplotlib
<https://matplotlib.org/>`_, `NetworkX
<https://networkx.org/>`_, `NumPy <https://numpy.org/>`_,
`SciPy <https://www.scipy.org/index.html>`_,
`Setuptools <https://setuptools.pypa.io/en/latest/>`_ and 
`SymPy <https://www.sympy.org>`_ packages. These can be
installed from `python.org <https://www.python.org/>`_ and `PyPI
<https://pypi.org/>`_, or via a package manager such as `Anaconda
<https://www.anaconda.com/>`_, `WinPython <https://winpython.github.io/>`_,
`MacPorts <https://www.macports.org/>`_, `HomeBrew <https://brew.sh/>`_,
`APT <https://en.wikipedia.org/wiki/APT_(software)>`_ etc.

Installation
------------

The easiest ways to install ``radioactivedecay`` are via the `Python Package
Index <https://pypi.org/project/radioactivedecay/>`_ using ``pip``:

.. code-block:: bash

    $ pip install radioactivedecay

or via `conda-forge <https://anaconda.org/conda-forge/radioactivedecay>`_:

.. code-block:: bash

    $ conda install -c conda-forge radioactivedecay

Either command will attempt to install the dependencies (Matplotlib, NetworkX,
NumPy, SciPy, Setuptools & SymPy) if they are not already present in the
environment.

It is also possible to clone the GitHub `repository 
<https://github.com/radioactivedecay/radioactivedecay>`_ and install from within the
``radioactivedecay`` directory using:

.. code-block:: bash

    $ pip install -e .

Testing
-------

``radioactivedecay`` includes code tests using the unittest framework. To run 
the tests, first git clone the repository from `GitHub
<https://github.com/radioactivedecay/radioactivedecay>`_:

.. code-block:: bash

    $ git clone https://github.com/radioactivedecay/radioactivedecay.git

then execute:

.. code-block:: bash

    $ cd radioactivedecay
    $ python -m unittest discover

Uninstallation
--------------

You can uninstall ``radioactivedecay`` by:

.. code-block:: bash

    $ pip uninstall radioactivedecay

or if installed originally via ``conda``:

.. code-block:: bash

    $ conda uninstall radioactivedecay
