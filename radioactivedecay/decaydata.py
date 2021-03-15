"""
The decaydata module defines the ``DecayData`` and ``DecayMatrices`` classes. Instances of
``DecayData`` initialize by reading in files containing radioactive decay data. The instances then
store the decay data, and their methods can be used for basic querying of the decay data.

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

Attributes
----------
DEFAULTDATA : DecayData
    Default radioactive decay dataset used by ``radioactivedecay``. This is currently ICRP-107.
"""

from pathlib import Path
import pickle
from typing import ContextManager, Union
import numpy as np
from scipy import sparse
from sympy import log, Matrix
from sympy.core.numbers import Rational
from sympy.matrices import SparseMatrix
from radioactivedecay.utils import parse_nuclide, parse_radionuclide, time_unit_conv

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def _get_package_filepath(dataset: str, filename: str) -> ContextManager[Path]:
    """
    Returns the path to a decay dataset file which is bundled as a sub-package within the
    ``radioactivedecay`` package.

    Parameters
    ----------
    dataset : str
        Name of the decay dataset.
    filename : str
        Name of the file.

    Returns
    -------
    ContextManager[Path]
        A context manager providing a file path object for the decay dataset file.
    """

    with resources.path(__package__ + "." + dataset, filename) as package_path:
        return package_path


def _get_package_pickle(dataset: str, filename: str) -> Union[Matrix, SparseMatrix]:
    """
    Returns an object loaded from a decay dataset file which is bundled as a sub-package within the
    ``radioactivedecay`` package.

    Parameters
    ----------
    dataset : str
        Name of the decay dataset.
    filename : str
        Name of the file.

    Returns
    -------
    Matrix or SparseMatrix
        A SymPy dense or sparse matrix loaded from the decay dataset pickle file.
    """

    with resources.open_binary(__package__ + "." + dataset, filename) as file:
        return pickle.load(file)


def _csr_matrix_equal(matrix_a: sparse.csr_matrix, matrix_b: sparse.csr_matrix) -> bool:
    """
    Checks whether two SciPy Compressed Sparse Row (CSR) matrices have the same elements and that
    all the elements are equal.

    Parameters
    ----------
    matrix_a : scipy.sparse.csr.csr_matrix
        First SciPy CSR matrix.
    matrix_b : scipy.sparse.csr.csr_matrix
        Second SciPy CSR matrix.

    Returns
    -------
    bool
        True if both CSR matrices have the same elements and they are all equal, False otherwise.
    """

    return (
        np.array_equal(matrix_a.indptr, matrix_b.indptr)
        and np.array_equal(matrix_a.indices, matrix_b.indices)
        and np.array_equal(matrix_a.data, matrix_b.data)
    )


class DecayMatrices:
    """
    Instances of DecayMatrices store matrices and vectors used for decay calculations, and the
    conversion for the number of days in a year which is specific to the decay dataset.
    DecayMatrices instances store data in either double precision SciPy/NumPy objects or
    arbitrary-precision SymPy objects.

    Parameters
    ----------
    decay_consts : numpy.ndarray or sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (s\\ :sup:`-1`).
    matrix_c : scipy.sparse.csr.csr_matrix or sympy.matrices.sparse.MutableSparseMatrix
        A pre-calculated sparse lower traingular matrix used in decay calculations.
    matrix_c_inv : scipy.sparse.csr.csr_matrix or sympy.matrices.sparse.MutableSparseMatrix
        The inverse of matrix_c, also used in decay calculations.
    year_conv : float or sympy.core.numbers.Rational
        Conversion factor for number of days in one year.

    Attributes
    ----------
    decay_consts : numpy.ndarray or sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (s\\ :sup:`-1`).
    ln2: float or log
        Constant natural logarithm of 2.
    matrix_c : scipy.sparse.csr.csr_matrix or sympy.matrices.sparse.MutableSparseMatrix
        A precalculated sparse lower triangular matrix used in decay calculations.
    matrix_c_inv : scipy.sparse.csr.csr_matrix or sympy.matrices.sparse.MutableSparseMatrix
        The inverse of matrix_c, also used in decay calculations.
    matrix_e : scipy.sparse.csr.csr_matrix or sympy.matrices.sparse.MutableSparseMatrix
        The matrix exponential that is used in radioactive decay calculations. It is a diagonal
        matrix that is pre-allocted for performance reasons.
    vector_n0 : numpy.ndarray or sympy.matrices.dense.MutableDenseMatrix
        Column vector for the number of atoms of each radionuclide. It is pre-allocted for
        performance reasons.
    year_conv : float or sympy.core.numbers.Rational
        Conversion factor for number of days in one year.

    """

    def __init__(
        self,
        decay_consts: Union[np.ndarray, Matrix],
        matrix_c: Union[sparse.csr_matrix, SparseMatrix],
        matrix_c_inv: Union[sparse.csr_matrix, SparseMatrix],
        year_conv: Union[float, Rational],
    ) -> None:
        self.decay_consts = decay_consts
        self.matrix_c = matrix_c
        self.matrix_c_inv = matrix_c_inv
        self.year_conv = year_conv

        if isinstance(self.matrix_c, sparse.csr.csr_matrix):
            self.ln2 = np.log(2)
            self.matrix_e = sparse.csr_matrix(
                (
                    np.zeros(matrix_c.shape[0]),
                    (np.arange(matrix_c.shape[0]), np.arange(matrix_c.shape[1])),
                )
            )
            self.vector_n0 = np.zeros([matrix_c.shape[0]], dtype=np.float64)
        else:
            self.ln2 = log(2)
            self.matrix_e = SparseMatrix.zeros(matrix_c.shape[0], matrix_c.shape[1])
            self.vector_n0 = Matrix.zeros(matrix_c.shape[0], 1)

    def __eq__(self, other) -> bool:
        """
        Check whether two ``DecayMatrices`` instances are equal with ``==`` operator.
        """

        if isinstance(self.matrix_c, sparse.csr.csr_matrix):
            return (
                (self.decay_consts == other.decay_consts).all()
                and self.ln2 == other.ln2
                and _csr_matrix_equal(self.matrix_c, other.matrix_c)
                and _csr_matrix_equal(self.matrix_c_inv, other.matrix_c_inv)
                and _csr_matrix_equal(self.matrix_e, other.matrix_e)
                and (self.vector_n0 == other.vector_n0).all()
                and self.year_conv == other.year_conv
            )

        return (
            self.decay_consts == other.decay_consts
            and self.ln2 == other.ln2
            and self.matrix_c == other.matrix_c
            and self.matrix_c_inv == other.matrix_c_inv
            and self.matrix_e == other.matrix_e
            and self.vector_n0 == other.vector_n0
            and self.year_conv == other.year_conv
        )

    def __ne__(self, other) -> bool:
        """
        Check whether two ``DecayMatrices`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)

    def __repr__(self) -> str:

        if isinstance(self.matrix_c, sparse.csr.csr_matrix):
            return "DecayMatrices: data stored in SciPy/NumPy objects for double precision calculations."

        return "DecayMatrices: data stored in SymPy objects for arbitrary-precision calculations."


class DecayData:
    """
    Instances of DecayData store a complete radioactive decay dataset.

    Parameters
    ----------
    dataset : str
        Name of the decay dataset.
    dir_path : str or None, optional
        Path to the directory containing the decay dataset files. Use None if the data are bundled
        as a sub-package of ``radioactivedecay`` (default is None).
    load_sympy : bool, optional
        Load SymPy version of the decay data for arbitrary-precision decay calculations (default is
        False).

    Attributes
    ----------
    dataset : str
        Name of the decay dataset.
    hldata : numpy.ndarray
        List of tuples containing half-life floats and time unit strings.
    num_radionuclides : int
        Number of radionuclides in the dataset.
    radionuclides : numpy.ndarray
        NumPy array of radionuclides in the dataset (string format is 'H-3', etc.).
    radionuclide_dict : dict
        Dictionary containing radionuclide strings as keys and positions in the matrices as values.
    prog_bfs_modes : numpy.ndarray
        NumPy array of dictionaries with direct progeny as keys and lists with branching fraction
        and decay mode data as values.
    scipy_data : DecayMatrices
        Dataset of double precision decay matrices (SciPy/NumPy objects).
    sympy_data : None or DecayMatrices
        Dataset of arbitrary-precision decay matrices (SymPy objects). Or None if this functionality
        is not used.

    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self, dataset: str, dir_path: Union[str, None] = None, load_sympy: bool = False,
    ) -> None:

        self.dataset = dataset

        if dir_path is None:
            data = np.load(
                _get_package_filepath(self.dataset, "decay_data.npz"),
                allow_pickle=True,
            )
        else:
            data = np.load(dir_path + "/decay_data.npz", allow_pickle=True)

        self.radionuclides = data["radionuclides"]
        self.hldata = data["hldata"]
        self.prog_bfs_modes = data["prog_bfs_modes"]

        self.num_radionuclides = self.radionuclides.size
        self.radionuclide_dict = dict(
            zip(self.radionuclides, list(range(0, self.num_radionuclides)))
        )

        decay_consts = np.array(
            [
                np.log(2)
                / time_unit_conv(
                    hl[0], units_from=hl[1], units_to="s", year_conv=data["year_conv"]
                )
                for hl in self.hldata
            ]
        )

        if dir_path is None:
            matrix_c = sparse.load_npz(
                _get_package_filepath(self.dataset, "c_scipy.npz")
            )
            matrix_c_inv = sparse.load_npz(
                _get_package_filepath(self.dataset, "c_inv_scipy.npz")
            )
        else:
            matrix_c = sparse.load_npz(dir_path + "/c_scipy.npz")
            matrix_c_inv = sparse.load_npz(dir_path + "/c_inv_scipy.npz")
        self.scipy_data = DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, data["year_conv"]
        )

        if load_sympy:
            if dir_path is None:
                decay_consts = _get_package_pickle(
                    self.dataset, "decay_consts_sympy.pickle"
                )
                matrix_c = _get_package_pickle(self.dataset, "c_sympy.pickle")
                matrix_c_inv = _get_package_pickle(self.dataset, "c_inv_sympy.pickle")
                year_conv = _get_package_pickle(
                    self.dataset, "year_conversion_sympy.pickle"
                )
            else:
                with open(dir_path + "/decay_consts_sympy.pickle", "rb") as file:
                    decay_consts = pickle.load(file)
                with open(dir_path + "/c_sympy.pickle", "rb") as file:
                    matrix_c = pickle.load(file)
                with open(dir_path + "/c_inv_sympy.pickle", "rb") as file:
                    matrix_c_inv = pickle.load(file)
                with open(dir_path + "/year_conversion_sympy.pickle", "rb") as file:
                    year_conv = pickle.load(file)

            self.sympy_data: Union[None, DecayMatrices] = DecayMatrices(
                decay_consts, matrix_c, matrix_c_inv, year_conv
            )
        else:
            self.sympy_data = None

    def half_life(self, radionuclide: str, units: str = "s") -> Union[float, str]:
        """
        Returns the half-life of the radionuclide as a float in your chosen units, or as
        a human-readable string with appropriate units.

        Parameters
        ----------
        radionuclide : str
            Radionuclide string.
        units : str, optional
            Units for half-life. Options are 'ps', 'ns', 'μs', 'us', 'ms', 's', 'm', 'h', 'd', 'y',
            'ky', 'My', 'By', 'Gy', 'Ty', 'Py', and common spelling variations. Default is 's', i.e.
            seconds. Use 'readable' to get a string of the half-life in human-readable units.

        Returns
        -------
        float or str
            Radionuclide half-life.

        Examples
        --------
        >>> rd.DEFAULTDATA.half_life('Rn-222', 'd')
        3.8235
        >>> rd.DEFAULTDATA.half_life('H-3')
        388781329.30560005
        >>> rd.DEFAULTDATA.half_life('H-3', 'readable')
        '12.32 y'

        """

        radionuclide = parse_radionuclide(
            radionuclide, self.radionuclides, self.dataset
        )
        half_life, unit, readable_str = self.hldata[
            self.radionuclide_dict[radionuclide]
        ]

        if units == "readable":
            return readable_str

        return (
            half_life
            if unit == units
            else time_unit_conv(
                half_life,
                units_from=unit,
                units_to=units,
                year_conv=self.scipy_data.year_conv,
            )
        )

    def branching_fraction(self, parent: str, progeny: str) -> float:
        """
        Returns the branching fraction for parent to progeny (if it exists).

        Parameters
        ----------
        parent : str
            Radionuclide string of the parent.
        progeny : str
            Nuclide string of the progeny (can be stable or radioactive nuclide).

        Returns
        -------
        float
            Branching fraction (or zero if progeny is not actually a direct progeny of parent).

        Examples
        --------
        >>> rd.DEFAULTDATA.branching_fraction('K-40', 'Ca-40')
        0.8914

        """

        parent = parse_radionuclide(parent, self.radionuclides, self.dataset)
        progeny = parse_nuclide(progeny)
        if progeny in self.prog_bfs_modes[self.radionuclide_dict[parent]]:
            return self.prog_bfs_modes[self.radionuclide_dict[parent]][progeny][0]

        return 0.0

    def decay_mode(self, parent: str, progeny: str) -> str:
        """
        Returns the type of decay mode between parent and progeny (if one exists). Note: the decay
        mode string returned is not a list of all the different radiation types emitted during the
        decay process between parent and progeny. It is the label defined in the decay dataset to
        classify the decay type (e.g. '\u03b1', '\u03b2-' or 'IT').

        Parameters
        ----------
        parent : str
            Radionuclide string of the parent.
        progeny : str
            Nuclide string of the progeny (can be stable or radioactive nuclide).

        Returns
        -------
        str
            Decay mode (or '' if progeny is not actually a direct progeny of the parent).

        Examples
        --------
        >>> rd.DEFAULTDATA.decay_mode('K-40', 'Ca-40')
        '\u03b2-'

        """

        parent = parse_radionuclide(parent, self.radionuclides, self.dataset)
        progeny = parse_nuclide(progeny)
        if progeny in self.prog_bfs_modes[self.radionuclide_dict[parent]]:
            return self.prog_bfs_modes[self.radionuclide_dict[parent]][progeny][1]

        return ""

    def __eq__(self, other) -> bool:
        """
        Check whether two ``DecayData`` instances are equal with ``==`` operator.
        """

        return (
            self.dataset == other.dataset
            and (self.hldata == other.hldata).all()
            and self.num_radionuclides == other.num_radionuclides
            and (self.radionuclides == other.radionuclides).all()
            and self.radionuclide_dict == other.radionuclide_dict
            and (self.prog_bfs_modes == other.prog_bfs_modes).all()
            and self.scipy_data == other.scipy_data
            and self.sympy_data == other.sympy_data
        )

    def __ne__(self, other) -> bool:
        """
        Check whether two ``DecayData`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)

    def __repr__(self) -> str:
        return (
            "Decay dataset: " + self.dataset + ", contains SymPy data: False"
            if self.sympy_data is None
            else "Decay dataset: " + self.dataset + ", contains SymPy data: True"
        )


DEFAULTDATA = DecayData("icrp107", load_sympy=True)
