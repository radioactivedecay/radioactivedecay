"""
The inventory module defines the ``Inventory`` class. Each ``Inventory`` instance contains one or
more radionuclides, each with an assoicated activity. The decay of the radionuclide(s) in an
``Inventory`` can be calculated by using the ``decay()`` method. A ``DecayData`` dataset is
associated with each ``Inventory`` instance (default is DEFAULTDATA).

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from typing import Callable, Dict, List, Union
from radioactivedecay.decaydata import DecayData, DEFAULTDATA, np
from radioactivedecay.radionuclide import Radionuclide
from radioactivedecay.utils import (
    parse_radionuclide,
    time_unit_conv,
    add_dictionaries,
    method_dispatch,
)


def check_dictionary(
    input_inv_dict: Dict[Union[str, Radionuclide], float],
    radionuclides: List[str],
    dataset: str,
) -> Dict[str, float]:
    """
    Checks validity of a dictionary of radionuclides and associated acitivities. Radionuclides
    must be in the decay dataset. Radionuclide strings are parsed to to Ab-XX format.

    Parameters
    ----------
    input_inv_dict : dict
        Dictionary containing radionuclide strings or Radionuclide objects as keys and activities
        as values.
    radionuclides : List[str]
        List of all the radionuclides in the decay dataset.
    dataset : str
        Name of the decay dataset.

    Returns
    -------
    dict
        Dictionary where the contents have been validated and the keys (radionuclide strings) have
        been parsed into symbol - mass number format.

    Raises
    ------
    ValueError
        If an activity key is invalid.

    Examples
    --------
    >>> rd.inventory.check_dictionary({'3H': 1.0}, rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    {'H-3': 1.0}
    >>> H3 = rd.Radionuclide('H-3')
    >>> rd.inventory.check_dictionary({H3: 1.0}, rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    {'H-3': 1.0}

    """

    inv_dict: Dict[str, float] = {
        (
            parse_radionuclide(nuc.radionuclide, radionuclides, dataset)
            if isinstance(nuc, Radionuclide)
            else parse_radionuclide(nuc, radionuclides, dataset)
        ): act
        for nuc, act in input_inv_dict.items()
    }
    for nuc, act in inv_dict.items():
        if not isinstance(act, (float, int)):
            raise ValueError(
                str(act) + " is not a valid radioactivity for " + str(nuc) + "."
            )

    return inv_dict


class Inventory:
    """
    ``Inventory`` instances store a dictionary of radionuclides and associated activities, and a
    ``DecayData`` instance of radioactive decay data.

    Parameters
    ----------
    contents : dict
        Dictionary containing radionuclide strings or Radionuclide objects as keys and activities
        as values.
    check : bool, optional
        Check for the validity of contents (default is True).
    data : DecayData, optional
        Decay dataset (default is the ICRP-107 dataset).

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
    Inventory: {'I-123': 5.8, 'Tc-99m': 2.3}, decay dataset: icrp107
    >>> H3 = rd.Radionuclide('H-3')
    >>> rd.Inventory({H3: 3.0})
    Inventory: {'H-3': 3.0}, decay dataset: icrp107

    """

    def __init__(
        self,
        contents: Dict[Union[str, Radionuclide], float],
        check: bool = True,
        data: DecayData = DEFAULTDATA,
    ) -> None:
        parsed_contents: Dict[str, float] = check_dictionary(
            contents, data.radionuclides, data.dataset
        ) if check is True else contents
        self.contents: Dict[str, float] = dict(
            sorted(parsed_contents.items(), key=lambda x: x[0])
        )
        self.data: DecayData = data

    def change(
        self,
        contents: Dict[Union[str, Radionuclide], float],
        check: bool,
        data: DecayData,
    ) -> None:
        """
        Changes the contents and data attritubes of this Inventory instance.
        """

        parsed_contents: Dict[str, float] = check_dictionary(
            contents, data.radionuclides, data.dataset
        ) if check is True else contents
        self.contents = dict(sorted(parsed_contents.items(), key=lambda x: x[0]))
        self.data = data

    @property
    def radionuclides(self) -> List[str]:
        """
        Returns a list of the radionuclides in the Inventory.

        Examples
        --------
        >>> rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8}).radionuclides
        ['I-123', 'Tc-99m']

        """

        return list(self.contents)

    @property
    def activities(self) -> List[float]:
        """
        Returns a list of the activities of the radionuclides in the Inventory.

        Examples
        --------
        >>> rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8}).activities
        [5.8, 2.3]

        """

        return list(self.contents.values())

    def __len__(self) -> int:
        """
        Returns number of radionuclides in this inventory.
        """

        return len(self.contents)

    def add(self, add_contents: Dict[Union[str, Radionuclide], float]) -> None:
        """
        Adds a dictionary of radionuclides and associated activities to this inventory.

        Parameters
        ----------
        add_contents : dict
            Dictionary containing radionuclide strings or Radionuclide objects as keys and
            activities as values which are added to the Inventory object.

        Examples
        --------
        >>> inv = rd.Inventory({'H-3': 1.0})
        >>> inv.add({'C-14': 2.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 1.0}

        """

        parsed_add_contents: Dict[str, float] = check_dictionary(
            add_contents, self.data.radionuclides, self.data.dataset
        )
        new_contents = add_dictionaries(self.contents, parsed_add_contents)
        self.change(new_contents, False, self.data)

    def subtract(self, sub_contents: Dict[Union[str, Radionuclide], float]) -> None:
        """
        Subtracts a dictionary of radionuclides and associated activities from this inventory.

        Parameters
        ----------
        sub_contents : dict
            Dictionary containing radionuclide strings or Radionuclide objects as keys and
            activities as values which are subtracted from the Inventory object.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 2.0, 'H-3': 1.0})
        >>> inv.subtract({'H-3': 1.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 0.0}

        """
        parsed_sub_contents: Dict[str, float] = check_dictionary(
            sub_contents, self.data.radionuclides, self.data.dataset
        )
        parsed_sub_contents.update(
            (nuclide, radioactivity * -1.0)
            for nuclide, radioactivity in parsed_sub_contents.items()
        )
        new_contents = add_dictionaries(self.contents, parsed_sub_contents)
        self.change(new_contents, False, self.data)

    def __add__(self, other: "Inventory") -> "Inventory":
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

    def __sub__(self, other: "Inventory") -> "Inventory":
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

    def __mul__(self, const: float) -> "Inventory":
        """
        Defines * operator to multiply all activities of radionuclides in an Inventory by a
        float or int.
        """

        new_contents = self.contents.copy()
        for nuclide, radioactivity in new_contents.items():
            new_contents[nuclide] = radioactivity * const
        return Inventory(new_contents, False, self.data)

    def __rmul__(self, const: float) -> "Inventory":
        """
        Defines * operator to multiply all activities of radionuclides in an Inventory by a
        float or int.
        """

        return self.__mul__(const)

    def __truediv__(self, const: float) -> "Inventory":
        """
        Defines / operator to divide all activities of radionuclides in an Inventory by a
        float or int.
        """

        return self.__mul__(1.0 / const)

    @method_dispatch
    def remove(
        self, delete: Union[str, Radionuclide, List[Union[str, Radionuclide]]]
    ) -> None:
        """
        Removes radionuclide(s) from this inventory.

        Parameters
        ----------
        delete : str or Radionuclide or list
            Radionuclide string, Radionuclide object or list of radionuclide strings or
            Radionuclide Objects to delete from the Inventory object.

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
    def _(self, delete: str) -> Callable[[Dict[str, float], bool, DecayData], None]:
        """Remove radionuclide string from this inventory."""
        delete = parse_radionuclide(delete, self.data.radionuclides, self.data.dataset)
        new_contents = self.contents.copy()
        if delete not in new_contents:
            raise ValueError(delete + " does not exist in this inventory.")
        new_contents.pop(delete)
        self.change(new_contents, False, self.data)

    @remove.register(Radionuclide)
    def _(
        self, delete: Radionuclide
    ) -> Callable[[Dict[str, float], bool, DecayData], None]:
        """Remove radionuclide string from this inventory."""
        delete = parse_radionuclide(
            delete.radionuclide, self.data.radionuclides, self.data.dataset
        )
        new_contents = self.contents.copy()
        if delete not in new_contents:
            raise ValueError(delete + " does not exist in this inventory.")
        new_contents.pop(delete)
        self.change(new_contents, False, self.data)

    @remove.register(list)
    def _(
        self, delete: List[Union[str, Radionuclide]]
    ) -> Callable[[Dict[str, float], bool, DecayData], None]:
        """Remove list of radionuclide(s) from this inventory."""
        delete = [
            parse_radionuclide(
                nuc.radionuclide, self.data.radionuclides, self.data.dataset
            )
            if isinstance(nuc, Radionuclide)
            else parse_radionuclide(nuc, self.data.radionuclides, self.data.dataset)
            for nuc in delete
        ]
        new_contents = self.contents.copy()
        for nuc in delete:
            if nuc not in new_contents:
                raise ValueError(nuc + " does not exist in this inventory.")
            new_contents.pop(nuc)
        self.change(new_contents, False, self.data)

    def decay(self, decay_time: float, units: str = "s") -> "Inventory":
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

        vector_n0 = np.zeros([self.data.num_radionuclides], dtype=np.float64)
        indices_set = set()
        for radionuclide in self.contents:
            i = self.data.radionuclide_dict[radionuclide]
            vector_n0[i] = self.contents[radionuclide] / self.data.decay_consts[i]
            indices_set.update(self.data.matrix_c[:, i].nonzero()[0])
        indices = list(indices_set)

        matrix_e = self.data.matrix_e.copy()
        matrix_e.data[indices] = np.exp(
            np.multiply(-decay_time, self.data.decay_consts[indices])
        )
        vector_nt = (
            (self.data.matrix_c.dot(matrix_e)).dot(self.data.matrix_c_inv)
        ).dot(vector_n0)
        vector_at = np.multiply(vector_nt, self.data.decay_consts)

        new_contents = dict(zip(self.data.radionuclides[indices], vector_at[indices]))
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))
        return Inventory(new_contents, False, self.data)

    def half_lives(self, units: str = "s") -> Dict[str, float]:
        """
        Returns dictionary of half-lives of the radionuclides in the Inventory in chosen time
        units.

        Parameters
        ----------
        units : str, optional
            Units for half-life (default is seconds). Options are 'ns', 'us', 'ms', 's', 'm', 'h',
            'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common spelling variations of
            these time units.

        Returns
        -------
        dict
            Dictionary with radionuclide strings as keys and half-life floats as values.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 1.0, 'K-40': 2.0})
        >>> inv.half_lives('y')
        {'C-14': 5700.0, 'K-40': 1251000000.0}

        """

        return {nuc: self.data.half_life(nuc, units) for nuc in self.contents}

    def progeny(self) -> Dict[str, List[str]]:
        """
        Returns dictionary with the direct progeny of the radionuclides in the Inventory.

        Returns
        -------
        dict
            Dictionary with radionuclide strings as keys and lists of the direct progeny of each
            radionuclide, ordered by decreasing branching fraction, as values.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 1.0, 'K-40': 2.0})
        >>> inv.progeny()
        {'C-14': ['N-14'], 'K-40': ['Ca-40', 'Ar-40'])

        """

        return {nuc: Radionuclide(nuc, self.data).progeny() for nuc in self.contents}

    def branching_fractions(self) -> Dict[str, List[float]]:
        """
        Returns dictionary with the branching fractions of the direct progeny of the radionuclides
        in the Inventory.

        Returns
        -------
        dict
            Dictionary with radionuclide strings as keys and lists of the branching fractions to
            the direct progeny of each radionuclide as values.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 1.0, 'K-40': 2.0})
        >>> inv.branching_fractions()
        {'C-14': [1.0], 'K-40': [0.8914, 0.1086])

        """

        return {
            nuc: Radionuclide(nuc, self.data).branching_fractions()
            for nuc in self.contents
        }

    def decay_modes(self) -> Dict[str, List[str]]:
        """
        Returns dictionary with the decay modes of the direct progeny of the radionuclides in the
        Inventory. Note: the decay modes are not lists of all the different radiation types emitted
        by the decay.

        Returns
        -------
        dict
            Dictionary with radionuclide strings as keys and lists of the decay modes of the parent
            radionuclide

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 1.0, 'K-40': 2.0})
        >>> inv.decay_modes()
        {'C-14': ['\u03b2-'], 'K-40': ['\u03b2-', '\u03b2+ \u0026 EC'])

        """

        return {
            nuc: Radionuclide(nuc, self.data).decay_modes() for nuc in self.contents
        }

    def __repr__(self) -> str:
        return (
            "Inventory: " + str(self.contents) + ", decay dataset: " + self.data.dataset
        )

    def __eq__(self, other) -> bool:
        """
        Check whether two ``Inventory`` instances are equal with ``==`` operator.
        """

        return self.contents == other.contents and self.data == other.data

    def __ne__(self, other) -> bool:
        """
        Check whether two ``Inventory`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)
