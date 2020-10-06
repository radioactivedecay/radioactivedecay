"""
The decacyfunctions module defines the two main classes used by users: the ``Inventory`` and
``Radionuclide`` classes. It also contains functions to parse radionuclide strings, check the
validity of inventory dictionaries, and convert between time units.

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

Attributes
----------
DEFAULTDATA : DecayData
    Default decay dataset used by ``radioactivedecay``. This is currently ICRP 107.
"""

from functools import singledispatch, update_wrapper
import numpy as np
from radioactivedecay.decaydata import DecayData

DEFAULTDATA = DecayData("icrp107")


def parse_nuclide_name(nuclide_name, nuclide_names, dataset):
    """
    Parses a radionuclide string and checks whether the radionuclide is contained in the decay
    dataset.

    Parameters
    ----------
    nuclide_name : str
        Radionuclide string.
    nuclide_names : numpy.ndarray
        NumPy array of all the radionuclides in the decay dataset.
    dataset : str
        Name of the decay dataset.

    Returns
    -------
    str
        Radionuclide string parsed in symbol - mass number format.

    Raises
    ------
    ValueError
        If the radionuclide string is invalid or it is not contained in the decay dataset.

    Examples
    --------
    >>> rd.parse_nuclide_name('222Rn', rd.DEFAULTDATA.nuclide_names, rd.DEFAULTDATA.dataset)
    'Rn-222'
    >>> rd.parse_nuclide_name('Ba137m', rd.DEFAULTDATA.nuclide_names, rd.DEFAULTDATA.dataset)
    'Ba-137m'

    """

    letter_flag, number_flag = False, False
    for char in nuclide_name:
        if char.isalpha():
            letter_flag = True
        if char.isdigit():
            number_flag = True
        if letter_flag and number_flag:
            break

    if (
        not (letter_flag and number_flag)
        or len(nuclide_name) < 2
        or len(nuclide_name) > 7
    ):
        raise ValueError(
            str(nuclide_name)
            + " is not a valid radionuclide in"
            + dataset
            + " dataset."
        )

    original_nuclide_name = nuclide_name

    while nuclide_name[0].isdigit():  # Re-order inputs e.g. 99mTc to Tc99m.
        nuclide_name = nuclide_name[1:] + nuclide_name[0]
    if nuclide_name[0] in ["m", "n"]:
        nuclide_name = nuclide_name[1:] + nuclide_name[0]

    for i in range(1, len(nuclide_name)):  # Add hyphen e.g. Tc99m to Tc-99m.
        if nuclide_name[i].isdigit():
            if nuclide_name[i - 1] != "-":
                nuclide_name = nuclide_name[:i] + "-" + nuclide_name[i:]
            break

    if nuclide_name not in nuclide_names:
        raise ValueError(
            str(original_nuclide_name)
            + " is not a valid radionuclide in "
            + dataset
            + " dataset."
        )

    return nuclide_name


def check_dictionary(inv_dict, nuclide_names, dataset):
    """
    Checks validity of a dictionary of radionuclides and associated acitivities. Radionuclides
    must be in the decay dataset.

    Parameters
    ----------
    inv_dict : dict
        Dictionary containing radionuclide strings as keys and activities as values.
    nuclide_names : list or numpy.ndarray
        NumPy array of all the radionuclides in the decay dataset.
    dataset : str
        Name of the decay dataset.

    Returns
    -------
    dict
        Dictionary where the contents have been validated and the radionuclide key strings have
        been parsed into symbol - mass number format.

    Raises
    ------
    ValueError
        If an activity key is invalid.

    Examples
    --------
    >>> rd.check_dictionary({'3H': 1.0}, rd.DEFAULTDATA.nuclide_names, rd.DEFAULTDATA.dataset)
    {'H-3': 1.0}


    """

    inv_dict = {
        parse_nuclide_name(nuc, nuclide_names, dataset): act
        for nuc, act in inv_dict.items()
    }
    for nuc, act in inv_dict.items():
        if not isinstance(act, (float, int)):
            raise ValueError(
                str(act) + " is not a valid radioactivity for " + str(nuc) + "."
            )

    return inv_dict


def time_unit_conv(time, units_from, units_to, year_conv):
    """
    Converts a time from one set of units to another.

    Parameters
    ----------
    time : float
        Time before conversion.
    units_from : str
        Time unit before conversion
    units_to : str
        Time unit after conversion
    yeav_conv : float or int
        Conversion factor for number of days in a year.

    Returns
    -------
    float
        Time in new units.

    Raises
    ------
    ValueError
        If one of the time unit parameters is invalid.

    Examples
    --------
    >>> rd.time_unit_conv(1.0, 'd', 'h', rd.DEFAULTDATA.year_conv)
    24.0

    """

    conv = {
        "ns": 1.0e-9,
        "us": 1.0e-6,
        "ms": 1.0e-3,
        "s": 1.0,
        "m": 60.0,
        "h": 3600.0,
        "d": 86400.0,
        "y": 86400.0 * year_conv,
        "sec": 1,
        "second": 1,
        "seconds": 1,
        "hr": 3600.0,
        "hour": 3600.0,
        "hours": 3600.0,
        "day": 86400.0,
        "days": 86400.0,
        "yr": 86400.0 * year_conv,
        "year": 86400.0 * year_conv,
        "years": 86400.0 * year_conv,
        "ky": 86400.0 * year_conv * 1.0e3,
        "My": 86400.0 * year_conv * 1.0e6,
        "Gy": 86400.0 * year_conv * 1.0e9,
        "Ty": 86400.0 * year_conv * 1.0e12,
        "Py": 86400.0 * year_conv * 1.0e15,
    }

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )

    return time * conv[units_from] / conv[units_to]


def add_dictionaries(dict1, dict2):
    """Adds together two dictionaries of radionuclies and associated acitivities."""

    new_dict = dict1.copy()
    for nuclide, radioactivity in dict2.items():
        if nuclide in new_dict:
            new_dict[nuclide] = new_dict[nuclide] + radioactivity
        else:
            new_dict[nuclide] = radioactivity

    return new_dict


def method_dispatch(func):
    """Adds singledispatch support for class methods."""

    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class Inventory:
    """
    Inventory instances store a dictionary of radionuclides and associated activities, and a
    DecayData object of radioactive decay data.

    Parameters
    ----------
    contents : dict
        Dictionary containing radionuclide strings as keys and activities as values.
    check : bool, optional
        Check for the validity of contents (default is True).
    data : DecayData, optional
        Decay dataset (default is the ICRP 107 dataset).

    Attributes
    ----------
    contents : dict
        Dictionary containing radionuclide strings as keys and activities as values. Radionuclides
        in contents are sorted alphabetically.
    data : DecayData
        Decay dataset.

    Examples
    --------
    >>> rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
    Inventory: {'I-123': 5.8, 'Tc-99m': 2.3}, Decay dataset: icrp107

    """

    def __init__(self, contents, check=True, data=DEFAULTDATA):
        self.change(contents, check, data)

    def change(self, contents, check, data):
        """
        Changes or initializes the contents and data attritubes of this Inventory instance.
        """

        if check is True:
            contents = check_dictionary(contents, data.nuclide_names, data.dataset)
        self.contents = dict(sorted(contents.items(), key=lambda x: x[0]))
        self.data = data

    @property
    def radionuclides(self):
        """
        Returns a list of the radionuclides in the Inventory.

        Examples
        --------
        >>> rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8}).radionuclides
        ['I-123', 'Tc-99m']

        """

        return list(self.contents)

    @property
    def activities(self):
        """
        Returns a list of the radionuclides in the Inventory.

        Examples
        --------
        >>> rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8}).activities
        [5.8, 2.3]

        """

        return list(self.contents.values())

    def add(self, add_contents):
        """
        Adds a dictionary of radionuclides and associated activities to this inventory.

        Parameters
        ----------
        add_contents : dict
            Dictionary containing radionuclide strings as keys and activities as values which are
            added to the Inventory object.

        Examples
        --------
        >>> inv = rd.Inventory({'H-3': 1.0})
        >>> inv.add({'C-14': 2.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 1.0}

        """

        add_contents = check_dictionary(
            add_contents, self.data.nuclide_names, self.data.dataset
        )
        new_contents = add_dictionaries(self.contents, add_contents)
        self.change(new_contents, False, self.data)

    def subtract(self, sub_contents):
        """
        Subtracts a dictionary of radionuclides and associated activities from this inventory.

        Parameters
        ----------
        sub_contents : dict
            Dictionary containing radionuclide strings as keys and activities as values which are
            subtracted from the Inventory object.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 2.0, 'H-3': 1.0})
        >>> inv.subtract({'H-3': 1.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 0.0}

        """
        sub_contents = check_dictionary(
            sub_contents, self.data.nuclide_names, self.data.dataset
        )
        sub_contents.update(
            (nuclide, radioactivity * -1.0)
            for nuclide, radioactivity in sub_contents.items()
        )
        new_contents = add_dictionaries(self.contents, sub_contents)
        self.change(new_contents, False, self.data)

    def __add__(self, other):
        """
        Defines + operator to add two Inventory objects together.
        """

        if self.data.dataset != other.data.dataset:
            raise ValueError(
                "Decay datasets do not match. inv1: "
                + self.data.dataset
                + " inv2: "
                + other.data.dataset
            )
        new_contents = add_dictionaries(self.contents, other.contents)
        return Inventory(new_contents, False, self.data)

    def __sub__(self, other):
        """
        Defines - operator to subtract one Inventory object from another.
        """

        if self.data.dataset != other.data.dataset:
            raise ValueError(
                "Decay datasets do not match. inv1: "
                + self.data.dataset
                + " inv2: "
                + other.data.dataset
            )
        sub_contents = other.contents.copy()
        sub_contents.update(
            (nuclide, radioactivity * -1.0)
            for nuclide, radioactivity in sub_contents.items()
        )
        new_contents = add_dictionaries(self.contents, sub_contents)
        return Inventory(new_contents, False, self.data)

    def __mul__(self, const):
        """
        Defines * operator to multiply all activities of radionuclides in an Inventory by a
        float or int.
        """

        new_contents = self.contents.copy()
        for nuclide, radioactivity in new_contents.items():
            new_contents[nuclide] = radioactivity * const
        return Inventory(new_contents, False, self.data)

    def __rmul__(self, const):
        """
        Defines * operator to multiply all activities of radionuclides in an Inventory by a
        float or int.
        """

        return self.__mul__(const)

    def __truediv__(self, const):
        """
        Defines / operator to divide all activities of radionuclides in an Inventory by a
        float or int.
        """

        return self.__mul__(1.0 / const)

    @method_dispatch
    def remove(self, delete):
        """
        Removes radionuclide(s) from this inventory.

        Parameters
        ----------
        delete : str or list
            Radionuclide string or list of radionuclide strings to delete from the Inventory
            object.

        Examples
        --------
        >>> inv = rd.Inventory({'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0})
        >>> inv.remove('H-3')
        >>> inv.contents
        {'Be-10': 2.0, 'C-14': 3.0, 'K-40': 4.0}
        >>> inv.remove(['Be-10', 'K-40'])
        {'C-14': 3.0}

        """
        raise NotImplementedError("remove() takes string or list of radionuclides.")

    @remove.register(str)
    def _(self, delete):
        """Remove radionuclide string from this inventory."""
        delete = parse_nuclide_name(delete, self.data.nuclide_names, self.data.dataset)
        new_contents = self.contents.copy()
        if delete not in new_contents:
            raise ValueError(delete + " does not exist in this inventory.")
        new_contents.pop(delete)
        self.change(new_contents, False, self.data)

    @remove.register(list)
    def _(self, delete):
        """Remove list of radionuclide(s) from this inventory."""
        delete = [
            parse_nuclide_name(nuc, self.data.nuclide_names, self.data.dataset)
            for nuc in delete
        ]
        new_contents = self.contents.copy()
        for nuc in delete:
            if nuc not in new_contents:
                raise ValueError(nuc + " does not exist in this inventory.")
            new_contents.pop(nuc)
        self.change(new_contents, False, self.data)

    def decay(self, decay_time, units="s"):
        """
        Returns new Inventory resulting from radioactive decay of the current Inventory object for
        decay_time.

        Parameters
        ----------
        decay_time : float
            Decay time.
        units : str, optional
            Units of decay_time (default is seconds). Options are 'ns', 'us', 'ms', 's', 'm', 'h',
            'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common spelling variations of
            these time units.

        Returns
        -------
        Inventory
            New Inventory after radioactive decay.

        Examples
        --------
        >>> inv_t0 = rd.Inventory({'H-3': 1.0})
        >>> inv_t1 = inv_t0.decay(12.32, 'y')
        >>> inv_t1.contents
        {'H-3': 0.5}

        """

        decay_time = (
            decay_time
            if units == "s"
            else time_unit_conv(
                decay_time,
                units_from=units,
                units_to="s",
                year_conv=self.data.year_conv,
            )
        )

        vector_n0 = np.zeros([self.data.no_nuclides], dtype=np.float64)
        indices = set()
        for nuclide_name in self.contents:
            i = self.data.nuclide_dict[nuclide_name]
            vector_n0[i] = self.contents[nuclide_name] / self.data.decay_consts[i]
            indices.update(self.data.matrix_c[:, i].nonzero()[0])
        indices = list(indices)

        matrix_e = self.data.matrix_e.copy()
        matrix_e.data[indices] = np.exp(
            np.multiply(-decay_time, self.data.decay_consts[indices])
        )
        vector_nt = (
            (self.data.matrix_c.dot(matrix_e)).dot(self.data.matrix_c_inv)
        ).dot(vector_n0)
        vector_at = np.multiply(vector_nt, self.data.decay_consts)

        new_contents = dict(zip(self.data.nuclide_names[indices], vector_at[indices]))
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))
        return Inventory(new_contents, False, self.data)

    def __repr__(self):
        return (
            "Inventory: " + str(self.contents) + ", Decay dataset: " + self.data.dataset
        )


class Radionuclide:
    """
    Radionuclide instances are used to fetch decay data on one radionuclide.

    Parameters
    ----------
    nuclide_name : str
        Radionuclide string.
    data : DecayData, optional
        Decay dataset (default is the ICRP 107 dataset).

    Attributes
    ----------
    nuclide_name : str
        Radionuclide string.
    decay_constant : numpy.float64
        Decay constant of the radionuclide (s\\ :sup:`-1`).
    data : DecayData
        Decay dataset.

    Examples
    --------
    >>> rd.Radionuclide('H-3')
    Radionuclide: H-3, Decay dataset: icrp107

    """

    ln2 = np.log(2)

    def __init__(self, nuclide_name, data=DEFAULTDATA):
        self.change(nuclide_name, data)

    def change(self, nuclide_name, data):
        """
        Changes or initializes the nuclide_name, decay_constant and data attritubes of this
        Radionuclide instance.
        """

        self.nuclide_name = parse_nuclide_name(
            nuclide_name, data.nuclide_names, data.dataset
        )
        self.decay_constant = data.decay_consts[data.nuclide_dict[self.nuclide_name]]
        self.data = data

    def half_life(self, units="s"):
        """
        Returns half-life of radionuclide in chosen units.

        Parameters
        ----------
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
        >>> Rn222 = rd.Radionuclide('Rn-222')
        >>> Rn222.half_life('d')
        3.8235

        """

        conv = (
            1.0
            if units == "s"
            else time_unit_conv(
                1.0, units_from="s", units_to=units, year_conv=self.data.year_conv
            )
        )
        return conv * Radionuclide.ln2 / self.decay_constant

    def __repr__(self):
        return (
            "Radionuclide: "
            + str(self.nuclide_name)
            + ", Decay dataset: "
            + self.data.dataset
        )
