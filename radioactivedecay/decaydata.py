"""
The decacydata module defines the ``DecayData`` class. Instances of ``DecayData`` initalize by
reading in dataset files containing radioactive decay data. The instances then store the decay
data, and their methods can be used for basic querying of the decay data.

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

import numpy as np
from scipy import sparse
from radioactivedecay.utils import parse_nuclide, parse_radionuclide, time_unit_conv

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


def get_package_filepath(dataset, filename):
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
    str
        Path of the decay dataset file.

    """

    with pkg_resources.path(__package__ + "." + dataset, filename) as package_path:
        return package_path


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
    matrix_c : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a lower traingular matrix with constant elements that are precalculated from decay
        constants and branching fractions.
    matrix_c_inv : scipy.sparse.csc.csc_matrix
        The inverse of matrix_c.
    matrix_e : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a diagonal matrix that is pre-allocted here for performance reasons.
    no_radionuclides : int
        Number of radionuclides in the dataset.
    radionuclides : numpy.ndarray
        NumPy array of all radionuclides in the dataset.
    radionuclide_dict : dict
        Dictionary containing radionuclide strings as keys and positions in the radionuclides array
        as values.
    prog_bfs_modes : numpy.ndarray
        NumPy array of dictionaries with first progeny as keys and list with branching fraction and
        decay mode as values.
    year_conv : float
        Conversion factor for number of days in one year.

    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, dataset, dir_path=None):
        self.dataset = dataset
        self.load_data(dir_path)

        self.ln2 = np.log(2)

    def load_data(self, dir_path):
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

        self.no_radionuclides = self.radionuclides.size
        self.radionuclide_dict = dict(
            zip(self.radionuclides, list(range(0, self.no_radionuclides)))
        )
        self.matrix_e = sparse.csc_matrix(
            (
                np.zeros(self.no_radionuclides),
                (np.arange(self.no_radionuclides), np.arange(self.no_radionuclides)),
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

    def half_life(self, radionuclide, units="s"):
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

    def branching_fraction(self, parent, progeny):
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
            Branching fraction (or zero if the progeny argument is not actually a direct progeny of
            the parent).

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

    def decay_mode(self, parent, progeny):
        """
        Returns type of decay mode for a parent to progeny decay.

        Parameters
        ----------
        parent : str
            Radionuclide string of parent.
        progeny : str
            Nuclide string of progeny (can be stable or radioactive nuclide).

        Returns
        -------
        str
            Decay mode type (or '' if the progeny argument is not actually a direct progeny of
            the parent).

        Examples
        --------
        >>> rd.DEFAULTDATA.branching_fraction('K-40', 'Ca-40')
        0.8914

        """

        parent = parse_radionuclide(parent, self.radionuclides, self.dataset)
        progeny = parse_nuclide(progeny)
        if progeny in self.prog_bfs_modes[self.radionuclide_dict[parent]]:
            return self.prog_bfs_modes[self.radionuclide_dict[parent]][progeny][1]

        return ""

    def __repr__(self):
        return "Decay dataset: " + self.dataset
