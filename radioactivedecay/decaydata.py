"""
The decaydata module defines the ``DecayData``, ``DecayMatrices`` and ``DecayMatricesSympy``
classes. ``DecayMatrices`` and ``DecayMatricesSympy`` instances store data used for decay
calculations and other inventory transformations (using double-precision floating point and SymPy
arbitrary precision numbers, respectively). ``DecayData`` instances store ``DecayMatrices``,
``DecayMatricesSympy`` and unit converter objects, along with other decay data for reporting to
users (this data is not used for calculations).

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

Constants
---------
DEFAULTDATA : DecayData
    Default radioactive decay dataset used by ``radioactivedecay``. This is currently ICRP-107 for
    decay data and AME2020 and Nubase2020 for atomic mass data.
"""

from pathlib import Path
import pickle
from typing import Any, ContextManager, Optional, Union
import numpy as np
from scipy import sparse
import sympy
from sympy import Matrix
from sympy.matrices import SparseMatrix
from radioactivedecay.converters import (
    UnitConverterFloat,
    UnitConverterSympy,
    QuantityConverter,
    QuantityConverterSympy,
)
from radioactivedecay.utils import parse_nuclide

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def _csr_matrix_equal(matrix_a: sparse.csr_matrix, matrix_b: sparse.csr_matrix) -> bool:
    """
    Checks whether two SciPy Compressed Sparse Row (CSR) matrices are equal (i.e. they have the
    same elements and all elements are equal).

    Parameters
    ----------
    matrix_a : scipy.sparse.csr.csr_matrix
        First SciPy CSR matrix.
    matrix_b : scipy.sparse.csr.csr_matrix
        Second SciPy CSR matrix.

    Returns
    -------
    bool
        True if both sparse matrices are equal, False otherwise.
    """

    return (
        np.array_equal(matrix_a.indptr, matrix_b.indptr)
        and np.array_equal(matrix_a.indices, matrix_b.indices)
        and np.array_equal(matrix_a.data, matrix_b.data)
    )


class DecayMatrices:
    """
    Instances of DecayMatrices store vectors with fundamental decay/atomic data and matrices used
    for decay calculations.

    Parameters
    ----------
    atomic_masses : numpy.ndarray
        Column vector of the atomic masses (in g/mol).
    decay_consts : numpy.ndarray
        Column vector of the decay constants (in s\\ :sup:`-1`).
    matrix_c : scipy.sparse.csr.csr_matrix
        A pre-calculated sparse lower traingular matrix used in decay calculations.
    matrix_c_inv : scipy.sparse.csr.csr_matrix
        The inverse of matrix_c, also used in decay calculations.

    Attributes
    ----------
    atomic_masses : numpy.ndarray
        Column vector of the atomic masses (in g/mol).
    decay_consts : numpy.ndarray
        Column vector of the decay constants (in s\\ :sup:`-1`).
    ln2: float
        Constant natural logarithm of 2.
    matrix_c : scipy.sparse.csr.csr_matrix
        A precalculated sparse lower triangular matrix used in decay calculations.
    matrix_c_inv : scipy.sparse.csr.csr_matrix
        The inverse of matrix_c, also used in decay calculations.
    matrix_e : scipy.sparse.csr.csr_matrix
        The matrix exponential that is used in radioactive decay calculations. It is a diagonal
        matrix that is pre-allocted for performance reasons.
    vector_n0 : numpy.ndarray
        Column vector for the number of atoms of each nuclide. It is pre-allocted here to improve
        the performance of decay calculations.

    """

    def __init__(
        self,
        atomic_masses: np.ndarray,
        decay_consts: np.ndarray,
        matrix_c: sparse.csr_matrix,
        matrix_c_inv: sparse.csr_matrix,
    ) -> None:
        self.atomic_masses = atomic_masses
        self.decay_consts = decay_consts
        self.ln2 = self._setup_ln2()
        self.matrix_c = matrix_c
        self.matrix_c_inv = matrix_c_inv
        self.matrix_e = self._setup_matrix_e(matrix_c.shape[0])
        self.vector_n0 = self._setup_vector_n0(matrix_c.shape[0])

    @staticmethod
    def _setup_ln2() -> float:
        """
        Returns NumPy ln2.
        """

        log2: float = np.log(2)
        return log2

    @staticmethod
    def _setup_matrix_e(size: int) -> sparse.csr_matrix:
        """
        Returns SciPy CSR sparse matrix template for matrix_e.
        """

        return sparse.csr_matrix(
            (
                np.zeros(size),
                (np.arange(size), np.arange(size)),
            )
        )

    @staticmethod
    def _setup_vector_n0(size: int) -> np.ndarray:
        """
        Returns NumPy array template for vector_n0.
        """

        return np.zeros([size], dtype=np.float64)

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``DecayMatrices`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, DecayMatrices):
            return NotImplemented
        return (
            np.array_equal(self.atomic_masses, other.atomic_masses)
            and np.array_equal(self.decay_consts, other.decay_consts)
            and self.ln2 == other.ln2
            and _csr_matrix_equal(self.matrix_c, other.matrix_c)
            and _csr_matrix_equal(self.matrix_c_inv, other.matrix_c_inv)
            and _csr_matrix_equal(self.matrix_e, other.matrix_e)
            and np.array_equal(self.vector_n0, other.vector_n0)
        )

    def __ne__(self, other: object) -> bool:
        """
        Check whether two ``DecayMatrices`` instances are not equal with ``!=`` operator.
        """

        if not isinstance(other, DecayMatrices):
            return NotImplemented
        return not self.__eq__(other)

    def __repr__(self) -> str:

        return (
            "DecayMatrices: data stored in SciPy/NumPy objects for double precision "
            "calculations."
        )


class DecayMatricesSympy(DecayMatrices):
    """
    Version of DecayMatrices using SymPy arbitrary precision operations.

    Parameters
    ----------
    atomic_masses : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the atomic masses (in g/mol).
    decay_consts : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (in s\\ :sup:`-1`).
    matrix_c : sympy.matrices.sparse.MutableSparseMatrix
        A pre-calculated sparse lower traingular matrix used in decay calculations.
    matrix_c_inv : sympy.matrices.sparse.MutableSparseMatrix
        The inverse of matrix_c, also used in decay calculations.

    Attributes
    ----------
    atomic_masses : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the atomic masses (in g/mol).
    decay_consts : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (in s\\ :sup:`-1`).
    ln2: sympy.log
        Constant natural logarithm of 2.
    matrix_c : sympy.matrices.sparse.MutableSparseMatrix
        A precalculated sparse lower triangular matrix used in decay calculations.
    matrix_c_inv : sympy.matrices.sparse.MutableSparseMatrix
        The inverse of matrix_c, also used in decay calculations.
    matrix_e : sympy.matrices.sparse.MutableSparseMatrix
        The matrix exponential that is used in radioactive decay calculations. It is a diagonal
        matrix that is pre-allocted for performance reasons.
    vector_n0 : sympy.matrices.dense.MutableDenseMatrix
        Column vector for the number of atoms of each nuclide. It is pre-allocted here to improve
        the performance of decay calculations.

    """

    @staticmethod
    def _setup_ln2() -> sympy.log:
        """
        Returns SymPy version of ln2.
        """

        return sympy.log(2)

    @staticmethod
    def _setup_matrix_e(size: int) -> Matrix:
        """
        Returns template for SymPy version of matrix_e.
        """

        return SparseMatrix.zeros(size, size)

    @staticmethod
    def _setup_vector_n0(size: int) -> Matrix:
        """
        Returns template for SymPy version of vector_n0.
        """

        return Matrix.zeros(size, 1)

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``DecayMatricesSympy`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, DecayMatricesSympy):
            return NotImplemented
        return (
            self.atomic_masses == other.atomic_masses
            and self.decay_consts == other.decay_consts
            and self.ln2 == other.ln2
            and self.matrix_c == other.matrix_c
            and self.matrix_c_inv == other.matrix_c_inv
            and self.matrix_e == other.matrix_e
            and self.vector_n0 == other.vector_n0
        )

    def __repr__(self) -> str:

        return (
            "DecayMatricesSympy: data stored in SymPy objects for arbitrary-precision "
            "calculations."
        )


class DecayData:
    """
    Instances of DecayData store a complete radioactive decay dataset. It stores data for decay
    calculations, inventory transformations and unit conversions using DecayMatrices,
    UnitConverterFloat, QuantityConverter, DecayMatricesSympy, UnitConverterSympy and
    QuantityConverterSympy objects. Other decay data which are reported to users but not used in
    calculations are stored in other instance attributes.

    Parameters
    ----------
    dataset_name : str
        Name of the decay dataset.
    bfs : numpy.ndarray
        NumPy array of lists with branching fraction data.
    hldata : numpy.ndarray
        List of tuples containing half-life floats, time unit strings and readable format half-life
        strings.
    modes : numpy.ndarray
        NumPy array of lists with decay mode data.
    nuclides : numpy.ndarray
        NumPy array of nuclides in the dataset (string format is 'H-3', etc.).
    progeny : numpy.ndarray
        NumPy array of lists with direct progeny data.
    scipy_data : DecayMatrices
        Dataset of double precision decay matrices (SciPy/NumPy objects).
    float_unit_converter : UnitConverterFloat
        Convert between units of a single quantity using floating point operations.
    sympy_data : None or DecayMatricesSympy
        Dataset of arbitrary-precision decay matrices (SymPy objects). Or None if SymPy
        functionality is not used. Default is None.
    sympy_unit_converter : None or UnitConverterSympy
        Convert between units of a single quantity using SymPy arbitrary precision operations.
        Default is None.

    Attributes
    ----------
    bfs : numpy.ndarray
        NumPy array of lists with branching fraction data.
    dataset_name : str
        Name of the decay dataset.
    float_quantity_converter : QuantityConverter
        Convert between quantities using floating point operations.
    float_unit_converter : UnitConverterFloat
        Convert between units of a single quantity using floating point operations.
    hldata : numpy.ndarray
        List of tuples containing half-life floats, time unit strings and readable format half-life
        strings.
    modes : numpy.ndarray
        NumPy array of lists with decay mode data.
    nuclides : numpy.ndarray
        NumPy array of nuclides in the dataset (string format is 'H-3', etc.).
    nuclide_dict : dict
        Dictionary containing nuclide strings as keys and positions in the matrices as values.
    progeny : numpy.ndarray
        NumPy array of lists with direct progeny data.
    scipy_data : DecayMatrices
        Dataset of double precision decay matrices (SciPy/NumPy objects).
    sympy_data : None or DecayMatricesSympy
        Dataset of arbitrary-precision decay matrices (SymPy objects). Or None if this functionality
        is not used.
    sympy_quantity_converter : None or QuantityConverterSympy
        Convert between quantities using SymPy arbitrary precision operations.
    sympy_unit_converter : None or UnitConverterSympy
        Convert between units of a single quantity using SymPy arbitrary precision operations.

    """

    def __init__(
        self,
        dataset_name: str,
        bfs: np.ndarray,
        hldata: np.ndarray,
        modes: np.ndarray,
        nuclides: np.ndarray,
        progeny: np.ndarray,
        scipy_data: DecayMatrices,
        float_unit_converter: UnitConverterFloat,
        sympy_data: Optional[DecayMatricesSympy] = None,
        sympy_unit_converter: Optional[UnitConverterSympy] = None,
    ) -> None:

        self.dataset_name = dataset_name
        self.bfs = bfs
        self.float_unit_converter = float_unit_converter
        self.hldata = hldata
        self.modes = modes
        self.nuclides = nuclides
        self.nuclide_dict = dict(zip(self.nuclides, list(range(0, self.nuclides.size))))
        self.progeny = progeny
        self.scipy_data = scipy_data

        self.float_quantity_converter = QuantityConverter(
            self.nuclide_dict,
            self.scipy_data.atomic_masses,
            self.scipy_data.decay_consts,
        )

        self.sympy_data: Optional[DecayMatricesSympy] = None
        self.sympy_unit_converter: Optional[UnitConverterSympy] = None
        self.sympy_quantity_converter: Optional[QuantityConverterSympy] = None

        if sympy_data and sympy_unit_converter:
            self.sympy_data = sympy_data
            self.sympy_unit_converter = sympy_unit_converter
            self.sympy_quantity_converter = QuantityConverterSympy(
                self.nuclide_dict,
                self.sympy_data.atomic_masses,
                self.sympy_data.decay_consts,
            )

    def half_life(self, nuclide: str, units: str = "s") -> Union[float, str]:
        """
        Returns the half-life of the nuclide as a float in your chosen units, or as
        a human-readable string with appropriate units.

        Parameters
        ----------
        nuclide : str
            Nuclide string.
        units : str, optional
            Units for half-life. Options are 'ps', 'ns', 'μs', 'us', 'ms', 's', 'm', 'h', 'd', 'y',
            'ky', 'My', 'By', 'Gy', 'Ty', 'Py', and common spelling variations. Default is 's', i.e.
            seconds. Use 'readable' to get a string of the half-life in human-readable units.

        Returns
        -------
        float or str
            Nuclide half-life.

        Examples
        --------
        >>> rd.DEFAULTDATA.half_life('Rn-222', 'd')
        3.8235
        >>> rd.DEFAULTDATA.half_life('H-3')
        388781329.30560005
        >>> rd.DEFAULTDATA.half_life('H-3', 'readable')
        '12.32 y'
        >>> rd.DEFAULTDATA.half_life('He-3')
        inf
        >>> rd.DEFAULTDATA.half_life('He-3', 'readable')
        'stable'

        """

        nuclide = parse_nuclide(nuclide, self.nuclides, self.dataset_name)
        half_life: float
        unit: str
        readable_str: str
        half_life, unit, readable_str = self.hldata[self.nuclide_dict[nuclide]]

        if units == "readable":
            return readable_str

        return (
            half_life
            if unit == units
            else self.float_unit_converter.time_unit_conv(
                half_life,
                units_from=unit,
                units_to=units,
            )
        )

    def branching_fraction(self, parent: str, progeny: str) -> float:
        """
        Returns the branching fraction for parent to progeny (if it exists).

        Parameters
        ----------
        parent : str
            Nuclide string of the parent.
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

        parent = parse_nuclide(parent, self.nuclides, self.dataset_name)
        progeny = parse_nuclide(progeny, self.nuclides, self.dataset_name)
        for idx, prog in enumerate(self.progeny[self.nuclide_dict[parent]]):
            if prog == progeny:
                branching_fraction: float = self.bfs[self.nuclide_dict[parent]][idx]
                return branching_fraction
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
            Nuclide string of the parent.
        progeny : str
            Nuclide string of the progeny.

        Returns
        -------
        str
            Decay mode (or '' if progeny is not actually a direct progeny of the parent).

        Examples
        --------
        >>> rd.DEFAULTDATA.decay_mode('K-40', 'Ca-40')
        '\u03b2-'

        """

        parent = parse_nuclide(parent, self.nuclides, self.dataset_name)
        progeny = parse_nuclide(progeny, self.nuclides, self.dataset_name)
        for idx, prog in enumerate(self.progeny[self.nuclide_dict[parent]]):
            if prog == progeny:
                decay_mode: str = self.modes[self.nuclide_dict[parent]][idx]
                return decay_mode
        return ""

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``DecayData`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, DecayData):
            return NotImplemented
        return (
            self.dataset_name == other.dataset_name
            and self.float_unit_converter == other.float_unit_converter
            and np.array_equal(self.hldata, other.hldata)
            and np.array_equal(self.nuclides, other.nuclides)
            and self.nuclide_dict == other.nuclide_dict
            and np.array_equal(self.progeny, other.progeny)
            and np.array_equal(self.bfs, other.bfs)
            and np.array_equal(self.modes, other.modes)
            and self.scipy_data == other.scipy_data
            and self.sympy_data == other.sympy_data
            and self.sympy_unit_converter == other.sympy_unit_converter
        )

    def __ne__(self, other: object) -> bool:
        """
        Check whether two ``DecayData`` instances are not equal with ``!=`` operator.
        """

        if not isinstance(other, DecayData):
            return NotImplemented
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return (
            "Decay dataset: " + self.dataset_name + ", contains SymPy data: False"
            if self.sympy_data is None
            else "Decay dataset: " + self.dataset_name + ", contains SymPy data: True"
        )


def _get_package_filepath(subpackage_dir: str, filename: str) -> ContextManager[Path]:
    """
    Returns the path to a file which is bundled as a sub-package within the
    ``radioactivedecay`` package.

    Parameters
    ----------
    subpackage_dir : str
        Name of the sub-package directory.
    filename : str
        Name of the file.

    Returns
    -------
    ContextManager[Path]
        A context manager providing a file path object for the decay dataset file.

    """

    with resources.path(__package__ + "." + subpackage_dir, filename) as package_path:
        return package_path


def _get_filepath(
    dataset_name: str, dir_path: Union[None, str], filename: str
) -> Union[str, ContextManager[Path]]:
    """
    Returns the path to a decay dataset file (located either within a sub-package of
    ``radioactivedecay`` or within a local system directory).

    Parameters
    ----------
    dataset_name : str
        Name of the decay dataset (also sub-package directory).
    dir_path : None or str
        Local directory containing dataset files, if not loading from a sub-package.
    filename : str
        Name of the file.

    Returns
    -------
    str or ContextManager[Path]
        A string or context manager with the file path for the decay dataset file.

    """

    if dir_path:
        return f"{dir_path}/{filename}"
    return _get_package_filepath(dataset_name, filename)


def _load_package_pickle_file(subpackage_dir: str, filename: str) -> Any:
    """
    Returns an object loaded from a pickle file which is bundled as a sub-package within the
    ``radioactivedecay`` package.

    Parameters
    ----------
    subpackage_dir : str
        Name of the sub-package directory.
    filename : str
        Name of the pickle file.

    Returns
    -------
    Object
        Object loaded from the pickle file.

    """

    with resources.open_binary(__package__ + "." + subpackage_dir, filename) as file:
        return pickle.load(file)


def _load_pickle_file(
    dataset_name: str, dir_path: Union[None, str], filename: str
) -> Any:
    """
    Load an object from a pickle file which is located either in a sub-package of
    ``radioactivedecay`` or within a local system directory.

    Parameters
    ----------
    dataset_name : str
        Name of the decay dataset (also sub-package directory).
    dir_path : None or str
        Local directory containing dataset files, if not loading from a sub-package.
    filename : str
        Name of the pickle file.

    Returns
    -------
    Object
        Object loaded from the pickle file.

    """

    if dir_path:
        with open(f"{dir_path}/{filename}", "rb") as file:
            obj = pickle.load(file)
        return obj
    return _load_package_pickle_file(dataset_name, filename)


def load_dataset(
    dataset_name: str, dir_path: Optional[str] = None, load_sympy: bool = False
) -> DecayData:
    """
    Load a decay dataset, either from a set of data files within a sub-packaged of
    ``radioactivedecay``, or by specifying a local directory containing the data files.

    Parameters
    ----------
    dataset_name : str
        Name of the decay dataset (or sub-package directory name).
    dir_path : None or str, optional
        Path to the directory containing the decay dataset files. Use None to load data that are
        bundled as a sub-package of ``radioactivedecay`` (dataset_name should match the
        sub-package name in this case). Default is None.
    load_sympy : bool, optional
        Load SymPy version of the decay data for arbitrary-precision decay calculations. Default is
        False.

    Returns
    -------
    DecayData
        A decay dataset used by ``radioactivedecay``.

    """

    data = np.load(
        _get_filepath(dataset_name, dir_path, "decay_data.npz"),
        allow_pickle=True,
    )

    float_unit_converter = UnitConverterFloat(data["year_conv"])
    decay_consts = np.array(
        [
            np.log(2)
            / float_unit_converter.time_unit_conv(hl[0], units_from=hl[1], units_to="s")
            for hl in data["hldata"]
        ]
    )

    matrix_c = sparse.load_npz(_get_filepath(dataset_name, dir_path, "c_scipy.npz"))
    matrix_c_inv = sparse.load_npz(
        _get_filepath(dataset_name, dir_path, "c_inv_scipy.npz")
    )

    scipy_data = DecayMatrices(data["masses"], decay_consts, matrix_c, matrix_c_inv)

    sympy_data = None
    sympy_unit_converter = None
    if load_sympy:
        sympy_pickle_version = "1.9" if sympy.__version__ >= "1.9" else "1.8"

        atomic_masses = _load_pickle_file(
            dataset_name, dir_path, f"atomic_masses_sympy_{sympy_pickle_version}.pickle"
        )
        decay_consts = _load_pickle_file(
            dataset_name, dir_path, f"decay_consts_sympy_{sympy_pickle_version}.pickle"
        )
        matrix_c = _load_pickle_file(
            dataset_name, dir_path, f"c_sympy_{sympy_pickle_version}.pickle"
        )
        matrix_c_inv = _load_pickle_file(
            dataset_name, dir_path, f"c_inv_sympy_{sympy_pickle_version}.pickle"
        )
        year_conv_sympy = _load_pickle_file(
            dataset_name,
            dir_path,
            f"year_conversion_sympy_{sympy_pickle_version}.pickle",
        )
        sympy_data = DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        sympy_unit_converter = UnitConverterSympy(year_conv_sympy)

    return DecayData(
        dataset_name,
        data["bfs"],
        data["hldata"],
        data["modes"],
        data["nuclides"],
        data["progeny"],
        scipy_data,
        float_unit_converter,
        sympy_data,
        sympy_unit_converter,
    )


DEFAULTDATA = load_dataset("icrp107_ame2020_nubase2020", load_sympy=True)
