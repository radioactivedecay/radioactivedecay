"""
The decacydata module defines the ``DecayData`` class. Instances of ``DecayData`` initalize by
reading in dataset files containing radioactive decay data. The instances then store the decay
data, and their methods can be used for basic querying of the decay data.

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

Attributes
----------
DEFAULTDATA : DecayData
    Default decay dataset used by ``radioactivedecay``. This is currently ICRP 107.
"""

from pathlib import Path
from typing import ContextManager, Union
import numpy as np
from scipy import sparse
from radioactivedecay.utils import parse_nuclide, parse_radionuclide, time_unit_conv

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


def get_package_filepath(dataset: str, filename: str) -> ContextManager[Path]:
    """
    Returns the path to a decay dataset file when the decay dataset is bundled as a sub-package
    within the ``radioactivedecay`` package.

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

    with pkg_resources.path(__package__ + "." + dataset, filename) as package_path:
        return package_path


def csc_matrix_equal(matrix1, matrix2):
    """
    Checks whether two SciPy Compressed Sparse Column (CSC) matrices are equal.
    """

    return (
        np.array_equal(matrix1.indptr, matrix2.indptr)
        and np.array_equal(matrix1.indices, matrix2.indices)
        and np.array_equal(matrix1.data, matrix2.data)
    )


class DecayData:
    """
    Instances of DecayData store a radioactive decay dataset.

    Parameters
    ----------
    dataset : str
        Name of the decay dataset.
    dir_path : str or None, optional
        Path to the directory containing the decay dataset files. Use None if the data are bundled
        as a sub-package of ``radioactivedecay`` (default is None).

    Attributes
    ----------
    dataset : str
        Name of the decay dataset.
    decay_consts : numpy.ndarray
        NumPy array of radionuclide decay constants.
    ln2: numpy.float64
        Constant natural logarithm of 2.
    matrix_c : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a lower traingular matrix with constant elements that are precalculated from decay
        constants and branching fractions.
    matrix_c_inv : scipy.sparse.csc.csc_matrix
        The inverse of matrix_c.
    matrix_e : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a diagonal matrix that is pre-allocted here for performance reasons.
    num_radionuclides : int
        Number of radionuclides in the dataset.
    radionuclides : numpy.ndarray
        NumPy array of all radionuclides in the dataset.
    radionuclide_dict : dict
        Dictionary containing radionuclide strings as keys and positions in the radionuclides array
        as values.
    prog_bfs_modes : numpy.ndarray
        NumPy array of dictionaries with direct progeny as keys and list with branching fraction and
        decay mode as values.
    year_conv : float
        Conversion factor for number of days in one year.

    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, dataset: str, dir_path: Union[str, None] = None) -> None:
        self.dataset = dataset
        self.load_data(dir_path)

        self.ln2 = np.log(2)

    def load_data(self, dir_path: Union[str, None]) -> None:
        """
        Reads in radioactive decay dataset files and puts the data into DecayData instance
        attributes.

        Parameters
        ----------
        dir_path : str or None
            Path to the directory containing the decay dataset files, or None if the data are
            bundled as a sub-package of ``radioactivedecay``.

        """

        if dir_path is None:
            data = np.load(
                get_package_filepath(self.dataset, "decay_data.npz"), allow_pickle=True,
            )
        else:
            data = np.load(dir_path + "/decay_data.npz", allow_pickle=True)
        self.radionuclides = data["radionuclides"]
        self.decay_consts = data["decay_consts"]
        self.prog_bfs_modes = data["prog_bfs_modes"]
        self.year_conv = data["year_conv"]

        self.num_radionuclides = self.radionuclides.size
        self.radionuclide_dict = dict(
            zip(self.radionuclides, list(range(0, self.num_radionuclides)))
        )
        self.matrix_e = sparse.csc_matrix(
            (
                np.zeros(self.num_radionuclides),
                (np.arange(self.num_radionuclides), np.arange(self.num_radionuclides)),
            )
        )

        if dir_path is None:
            self.matrix_c = sparse.load_npz(get_package_filepath(self.dataset, "c.npz"))
            self.matrix_c_inv = sparse.load_npz(
                get_package_filepath(self.dataset, "cinverse.npz")
            )
        else:
            self.matrix_c = sparse.load_npz(dir_path + "/c.npz")
            self.matrix_c_inv = sparse.load_npz(dir_path + "/cinverse.npz")

    def half_life(self, radionuclide: str, units: str = "s") -> float:
        """
        Returns half-life of a radionuclide in chosen units.

        Parameters
        ----------
        radionuclide : str
            Radionuclide string.
        units : str, optional
            Units for half-life (default is seconds). Options are 'ns', 'us', 'ms', 's', 'm', 'h',
            'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common spelling variations of
            these time units.

        Returns
        -------
        float
            Radionuclide half-life.

        Examples
        --------
        >>> rd.DEFAULTDATA.half_life('Rn-222')
        3.8235

        """

        conv = (
            1.0
            if units == "s"
            else time_unit_conv(
                1.0, units_from="s", units_to=units, year_conv=self.year_conv
            )
        )

        radionuclide = parse_radionuclide(
            radionuclide, self.radionuclides, self.dataset
        )
        return conv * self.ln2 / self.decay_consts[self.radionuclide_dict[radionuclide]]

    def branching_fraction(self, parent: str, progeny: str) -> float:
        """
        Returns branching fraction for a parent to progeny decay.

        Parameters
        ----------
        parent : str
            Radionuclide string of parent.
        progeny : str
            Nuclide string of progeny (can be stable or radioactive nuclide).

        Returns
        -------
        float
            Branching fraction (or zero if the progeny parameter is not actually a direct progeny
            of the parent).

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
        mode is not a list of all the different radiation types emitted when the parent
        radionuclide decays.

        Parameters
        ----------
        parent : str
            Radionuclide string of parent.
        progeny : str
            Type of decay of the parent yielding progeny.

        Returns
        -------
        str
            Decay mode (or '' if the progeny parameter is not actually a direct progeny of the
            parent).

        Examples
        --------
        >>> rd.DEFAULTDATA.decay_mode('K-40', 'Ca-40')
        ''\u03b2-'

        """

        parent = parse_radionuclide(parent, self.radionuclides, self.dataset)
        progeny = parse_nuclide(progeny)
        if progeny in self.prog_bfs_modes[self.radionuclide_dict[parent]]:
            return self.prog_bfs_modes[self.radionuclide_dict[parent]][progeny][1]

        return ""

    def __repr__(self) -> str:

        return "Decay dataset: " + self.dataset

    def __eq__(self, other) -> bool:
        """
        Check whether two ``DecayData`` instances are equal with ``==`` operator.
        """

        return (
            self.dataset == other.dataset
            and (self.decay_consts == other.decay_consts).all()
            and self.ln2 == other.ln2
            and csc_matrix_equal(self.matrix_c, other.matrix_c)
            and csc_matrix_equal(self.matrix_c_inv, other.matrix_c_inv)
            and csc_matrix_equal(self.matrix_e, other.matrix_e)
            and self.num_radionuclides == other.num_radionuclides
            and (self.radionuclides == other.radionuclides).all()
            and self.radionuclide_dict == other.radionuclide_dict
            and (self.prog_bfs_modes == other.prog_bfs_modes).all()
            and self.year_conv == other.year_conv
        )

    def __ne__(self, other) -> bool:
        """
        Check whether two ``DecayData`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)


DEFAULTDATA = DecayData("icrp107")
