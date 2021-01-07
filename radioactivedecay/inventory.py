"""
The inventory module defines the ``Inventory`` class. Each ``Inventory`` instance contains one or
more radionuclides, each with an associated activity. The decay of the radionuclide(s) in an
``Inventory`` can be calculated by using the ``decay()`` method (normal double-precision
floating-point operations). Use the ``decay_high_precision()`` method to perform a SymPy high
numerical precision calculation. A ``DecayData`` dataset associated with each ``Inventory``
instance is the radioactive decay data source (default is rd.DEFAULTDATA).

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from functools import singledispatch, update_wrapper
from typing import Callable, Dict, List, Union
from sympy import exp, nsimplify
from radioactivedecay.decaydata import DecayData, DEFAULTDATA, np
from radioactivedecay.radionuclide import Radionuclide
from radioactivedecay.utils import (
    parse_radionuclide,
    time_unit_conv,
    time_unit_conv_sympy,
)


def _add_dictionaries(
    dict_a: Dict[str, float], dict_b: Dict[str, float]
) -> Dict[str, float]:
    """
    Adds together two dictionaries of radionuclides and associated activities.

    Parameters
    ----------
    dict_a : dict
        First dictionary containing radionuclide strings as keys and activities as values.
    dict_b : dict
        Second dictionary containing radionuclide strings as keys and activities as values.

    Returns
    -------
    dict
        Combined dictionary containing the radionuclides in both dict_a and dict_b, where
        activities have been added together when a radionuclide is present in both input
        dictionaries.

    Examples
    --------
    >>> dict_a = {'Pm-141': 1.0, 'Rb-78': 2.0}
    >>> dict_b = {'Pm-141': 3.0, 'Rb-90': 4.0}
    >>> rd.inventory._add_dictionaries(dict_a, dict_b)
    {'Pm-141': 4.0, 'Rb-78': 2.0, 'Rb-90': 4.0}

    """

    new_dict = dict_a.copy()
    for radionuclide, radioactivity in dict_b.items():
        if radionuclide in new_dict:
            new_dict[radionuclide] = new_dict[radionuclide] + radioactivity
        else:
            new_dict[radionuclide] = radioactivity

    return new_dict


def _check_dictionary(
    input_inv_dict: Dict[Union[str, Radionuclide], float],
    radionuclides: List[str],
    dataset: str,
) -> Dict[str, float]:
    """
    Checks validity of a dictionary of radionuclides and associated activities. Radionuclides must
    be in the decay dataset. Radionuclide strings are parsed to to Ab-XX format.

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
    >>> rd.inventory._check_dictionary({'3H': 1.0}, rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    {'H-3': 1.0}
    >>> H3 = rd.Radionuclide('H-3')
    >>> rd.inventory._check_dictionary({H3: 1.0}, rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
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


def _method_dispatch(func):
    """Adds singledispatch support for class methods."""

    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


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

        self._change(contents, check, data)

    def _change(
        self,
        contents: Dict[Union[str, Radionuclide], float],
        check: bool,
        data: DecayData,
    ) -> None:
        """
        Changes the contents and data attributes of this Inventory instance.
        """

        parsed_contents: Dict[str, float] = _check_dictionary(
            contents, data.radionuclides, data.dataset
        ) if check is True else contents
        self.contents: Dict[str, float] = dict(
            sorted(parsed_contents.items(), key=lambda x: x[0])
        )
        self.data: DecayData = data

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
        Returns number of radionuclides in the inventory.
        """

        return len(self.contents)

    def add(self, add_contents: Dict[Union[str, Radionuclide], float]) -> None:
        """
        Adds a dictionary of radionuclides and associated activities to the inventory.

        Parameters
        ----------
        add_contents : dict
            Dictionary containing radionuclide strings or Radionuclide objects as keys and
            activities as values which are added to the Inventory.

        Examples
        --------
        >>> inv = rd.Inventory({'H-3': 1.0})
        >>> inv.add({'C-14': 2.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 1.0}

        """

        parsed_add_contents: Dict[str, float] = _check_dictionary(
            add_contents, self.data.radionuclides, self.data.dataset
        )
        new_contents = _add_dictionaries(self.contents, parsed_add_contents)
        self._change(new_contents, False, self.data)

    def subtract(self, sub_contents: Dict[Union[str, Radionuclide], float]) -> None:
        """
        Subtracts a dictionary of radionuclides and associated activities from this inventory.

        Parameters
        ----------
        sub_contents : dict
            Dictionary containing radionuclide strings or Radionuclide objects as keys and
            activities as values which are subtracted from the Inventory.

        Examples
        --------
        >>> inv = rd.Inventory({'C-14': 2.0, 'H-3': 1.0})
        >>> inv.subtract({'H-3': 1.0})
        >>> inv.contents
        {'C-14': 2.0, 'H-3': 0.0}

        """
        parsed_sub_contents: Dict[str, float] = _check_dictionary(
            sub_contents, self.data.radionuclides, self.data.dataset
        )
        parsed_sub_contents.update(
            (nuclide, radioactivity * -1.0)
            for nuclide, radioactivity in parsed_sub_contents.items()
        )
        new_contents = _add_dictionaries(self.contents, parsed_sub_contents)
        self._change(new_contents, False, self.data)

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
        new_contents = _add_dictionaries(self.contents, other.contents)
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
        new_contents = _add_dictionaries(self.contents, sub_contents)
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

    @_method_dispatch
    def remove(
        self, delete: Union[str, Radionuclide, List[Union[str, Radionuclide]]]
    ) -> None:
        """
        Removes radionuclide(s) from this inventory.

        Parameters
        ----------
        delete : str or Radionuclide or list
            Radionuclide string, Radionuclide object or list of radionuclide strings or
            Radionuclide objects to delete from the Inventory object.

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
        self._change(new_contents, False, self.data)

    @remove.register(Radionuclide)
    def _(
        self, delete: Radionuclide
    ) -> Callable[[Dict[str, float], bool, DecayData], None]:
        """Remove radionuclide object from this inventory."""

        delete = parse_radionuclide(
            delete.radionuclide, self.data.radionuclides, self.data.dataset
        )
        new_contents = self.contents.copy()
        if delete not in new_contents:
            raise ValueError(delete + " does not exist in this inventory.")
        new_contents.pop(delete)
        self._change(new_contents, False, self.data)

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
        self._change(new_contents, False, self.data)

    def decay(
        self, decay_time: float, units: str = "s", sig_fig: Union[None, int] = None
    ) -> "Inventory":
        """
        Returns a new Inventory calculated from the radioactive decay of the current Inventory for
        decay_time.

        Parameters
        ----------
        decay_time : float
            Decay time.
        units : str, optional
            Units of decay_time (default is seconds). Options are 'ns', 'us', 'ms', 's', 'm', 'h',
            'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common spelling variations of
            these time units.
        sig_fig: None or int, optional
            Performs a decay calculation using arbitrary-precision arithmetic with SymPy for this
            many significant figures. For high precision calculations, recommended is 320. sig_fig
            must be greater than 0. Default is None, which i standard SciPy/NumPy double precision
            calculations.

        Returns
        -------
        Inventory
            New Inventory after the radioactive decay.

        Raises
        ------
        ValueError
            If sig_fig is invalid or if the decay dataset associated with this Inventory
            (self.data) does not contain SymPy versions of the decay data.

        Examples
        --------
        >>> inv_t0 = rd.Inventory({'H-3': 1.0})
        >>> inv_t1 = inv_t0.decay(12.32, 'y')
        >>> inv_t1.contents
        {'H-3': 0.5}

        """

        if sig_fig is not None:
            if sig_fig < 1:
                raise ValueError("sig_fig needs to be an integer greater than 0.")
            if self.data.sympy_data is None:
                raise ValueError("No SymPy data in decay dataset " + self.data.dataset)
            return self._decay_sympy(decay_time, units, sig_fig)

        decay_time = (
            decay_time
            if units == "s"
            else time_unit_conv(
                decay_time,
                units_from=units,
                units_to="s",
                year_conv=self.data.scipy_data.year_conv,
            )
        )

        vector_n0 = self.data.scipy_data.vector_n0.copy()
        indices_set = set()
        for radionuclide in self.contents:
            i = self.data.radionuclide_dict[radionuclide]
            vector_n0[i] = (
                self.contents[radionuclide] / self.data.scipy_data.decay_consts[i]
            )
            indices_set.update(self.data.scipy_data.matrix_c[:, i].nonzero()[0])
        indices = list(indices_set)

        matrix_e = self.data.scipy_data.matrix_e.copy()
        matrix_e.data[indices] = np.exp(
            -decay_time * self.data.scipy_data.decay_consts[indices]
        )

        vector_nt = (
            self.data.scipy_data.matrix_c
            @ matrix_e
            @ self.data.scipy_data.matrix_c_inv
            @ vector_n0
        )
        vector_at = vector_nt[indices] * self.data.scipy_data.decay_consts[indices]

        new_contents = dict(zip(self.data.radionuclides[indices], vector_at))
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))

        return Inventory(new_contents, False, self.data)

    def decay_high_precision(self, decay_time: float, units: str = "s") -> "Inventory":
        """
        Decay calculation with high numerical precision. This uses SymPy arbitrary-precision
        arithmetic functions for the decay calculation. The results can be more accurate than
        a normal double precision float calculation (i.e. using ``decay(..., sig_fig=None)``) when
        the decay chains contain radionuclides with very similar half-lives or half-lives that
        differ by many orders of magnitude.

        This function requires that the decay dataset associated with the Inventory instance
        contains a SymPy version of the decay data. It uses sig_fig=320 for the SymPy calculation.

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
            New Inventory after the radioactive decay.

        Examples
        --------
        >>> inv_t0 = rd.Inventory({'Fm-257': 1.0})
        >>> inv_t1 = inv_t0.decay_high_precision(10.0, 'd')
        >>> inv_t1.contents
         {'Ac-225': 4.060286801476717e-51,
         'Am-241': 9.985270042416324e-24,
         'Am-245': 5.4061684195880344e-09,
         ...
         'Fm-257': 0.9333548028364793,
         ...
         }

        """

        return self.decay(decay_time, units, sig_fig=320)

    def _decay_sympy(self, decay_time: float, units: str, sig_fig: int) -> "Inventory":
        """
        Version of decay() using SymPy arbitrary-precision arithmetic.
        """

        decay_time = nsimplify(decay_time)

        decay_time = (
            decay_time
            if units == "s"
            else time_unit_conv_sympy(
                decay_time,
                units_from=units,
                units_to="s",
                year_conv=self.data.sympy_data.year_conv,
            )
        )

        vector_n0 = self.data.sympy_data.vector_n0.copy()
        indices_set = set()
        for radionuclide in self.contents:
            i = self.data.radionuclide_dict[radionuclide]
            vector_n0[i, 0] = (
                nsimplify(self.contents[radionuclide])
                / self.data.sympy_data.decay_consts[i, 0]
            )
            indices_set.update(self.data.scipy_data.matrix_c[:, i].nonzero()[0])
        indices = list(indices_set)

        matrix_e = self.data.sympy_data.matrix_e.copy()
        for i in indices:
            matrix_e[i, i] = exp(
                (-decay_time * self.data.sympy_data.decay_consts[i, 0]).evalf(sig_fig)
            )

        vector_nt = (
            self.data.sympy_data.matrix_c
            @ matrix_e
            @ self.data.sympy_data.matrix_c_inv
            @ vector_n0
        )

        new_contents = {}
        for i in indices:
            new_contents[self.data.radionuclides[i]] = float(
                vector_nt[i, 0] * self.data.sympy_data.decay_consts[i, 0]
            )
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))

        return Inventory(new_contents, False, self.data)

    def half_lives(self, units: str = "s") -> Dict[str, float]:
        """
        Returns dictionary of half-lives of the radionuclides in the Inventory in chosen time
        units.

        Parameters
        ----------
        units : str, optional
            Units for half-lives (default is 's', i.e. seconds). Options are 'ps', 'ns', 'us',
            'ms', 's', 'm', 'h', 'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common
            spelling variations of these time units.

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
        Inventory. Note: the decay mode strings returned are not lists of all the different
        radiation types emitted during the parent to progeny decay processes. They are the labels
        defined in the decay dataset to classify the decay type (e.g. '\u03b1', '\u03b2-' or 'IT').

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
