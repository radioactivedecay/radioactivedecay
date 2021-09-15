"""
The converters module contains classes for unit and quantity conversions.

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from abc import ABC, abstractmethod
from typing import Dict, Union
import numpy as np
from sympy import Integer, Matrix, nsimplify, Rational
from sympy.core.expr import Expr

AVOGADRO = 6.02214076e23


class UnitConverter(ABC):
    """
    Template class for unit converters using either floats or SymPy arithmetic.

    Parameters
    ----------
    year_conv : float or Rational
        Conversion factor for number of days in a year.

    Attributes
    ----------
    time_units : dict
        Dictionary containing numbers of each time unit per second.
    activity_units : dict
        Dictionary containing amounts of each activity unit per Bq.
    mass_units : dict
        Dictionary containing amounts of each mass unit per g.
    moles_units : dict
        Dictionary containing amounts of each mole unit per mol.

    """

    def __init__(self, year_conv: Union[float, Rational]):
        self.time_units = self.get_time_units(year_conv)
        self.activity_units = self.get_activity_units()
        self.mass_units = self.get_mass_units()
        self.moles_units = self.get_moles_units()

    @abstractmethod
    def get_time_units(
        self, year_conv: Union[float, Rational]
    ) -> Dict[str, Union[float, Expr]]:
        """
        Returns time units dictionary (template).
        """

        pass

    @abstractmethod
    def get_activity_units(self) -> Dict[str, Union[float, Expr]]:
        """
        Returns activity units dictionary (template).
        """

        pass

    @abstractmethod
    def get_mass_units(self) -> Dict[str, Union[float, Expr]]:
        """
        Returns mass units dictionary (template).
        """

        pass

    @abstractmethod
    def get_moles_units(self) -> Dict[str, Union[float, Expr]]:
        """
        Returns moles units dictionary (template).
        """

        pass

    def time_unit_conv(
        self, time_period: Union[float, Expr], units_from: str, units_to: str
    ) -> Union[float, Expr]:
        """
        Converts a time period from one time unit to another.

        Parameters
        ----------
        time_period : float or Expr
            Time period before conversion.
        units_from : str
            Time unit before conversion
        units_to : str
            Time unit after conversion

        Returns
        -------
        Expr
            Time period in new units.

        Raises
        ------
        ValueError
            If one of the time unit parameters is invalid.

        """

        if units_from not in self.time_units:
            raise ValueError(
                str(units_from)
                + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
            )
        if units_to not in self.time_units:
            raise ValueError(
                str(units_to) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
            )

        return time_period * self.time_units[units_from] / self.time_units[units_to]

    def activity_unit_conv(
        self, activity: Union[float, Expr], units_from: str, units_to: str
    ) -> Union[float, Expr]:
        """
        Converts an activity from one unit to another.

        Parameters
        ----------
        activity : float or Expr
            Activity before conversion.
        units_from : str
            Activity unit before conversion
        units_to : str
            Activity unit after conversion

        Returns
        -------
        Expr
            Activity in new units.

        Raises
        ------
        ValueError
            If one of the activity unit parameters is invalid.

        """

        if units_from not in self.activity_units:
            raise ValueError(
                str(units_from)
                + ' is not a valid activitiy unit, e.g. "Bq", "kBq", "Ci"...'
            )
        if units_to not in self.activity_units:
            raise ValueError(
                str(units_to) + ' is not a activitiy unit, e.g. "Bq", "kBq", "Ci"...'
            )

        return (
            activity * self.activity_units[units_from] / self.activity_units[units_to]
        )

    def mass_unit_conv(
        self, mass: Union[float, Expr], units_from: str, units_to: str
    ) -> Union[float, Expr]:
        """
        Converts a mass from one unit to another.

        Parameters
        ----------
        mass : float or Expr
            Mass before conversion.
        units_from : str
            Mass unit before conversion
        units_to : str
            Mass unit after conversion

        Returns
        -------
        Expr
            Mass in new units.

        Raises
        ------
        ValueError
            If one of the mass unit parameters is invalid.

        """

        if units_from not in self.mass_units:
            raise ValueError(
                str(units_from) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
            )
        if units_to not in self.mass_units:
            raise ValueError(
                str(units_to) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
            )

        return mass * self.mass_units[units_from] / self.mass_units[units_to]

    def moles_unit_conv(
        self, moles: Union[float, Expr], units_from: str, units_to: str
    ) -> Union[float, Expr]:
        """
        Converts a number of moles from one order of magnitude to another.

        Parameters
        ----------
        moles : float or Expr
            Amount before conversion.
        units_from : str
            Unit before conversion.
        units_to : str
            Unit after conversion.

        Returns
        -------
        Expr
            Result in chosen units.

        Raises
        ------
        ValueError
            If one of the unit parameters is invalid.

        """

        if units_from not in self.moles_units:
            raise ValueError(
                str(units_from) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
            )
        if units_to not in self.moles_units:
            raise ValueError(
                str(units_to) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
            )

        return moles * self.moles_units[units_from] / self.moles_units[units_to]

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``UnitConverter`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, UnitConverter):
            return NotImplemented
        return (
            self.time_units == other.time_units
            and self.activity_units == other.activity_units
            and self.mass_units == other.mass_units
            and self.moles_units == other.moles_units
        )

    def __ne__(self, other: object) -> bool:
        """
        Check whether two ``UnitConverter`` instances are not equal with ``!=`` operator.
        """

        if not isinstance(other, UnitConverter):
            return NotImplemented
        return not self.__eq__(other)


class UnitConverterFloat(UnitConverter):
    """
    Unit converter using floats.

    Parameters
    ----------
    year_conv : float
        Conversion factor for number of days in a year.

    Attributes
    ----------
    time_units : dict
        Dictionary containing numbers of each time unit per second.
    activity_units : dict
        Dictionary containing amounts of each activity unit per Bq.
    mass_units : dict
        Dictionary containing amounts of each mass unit per g.
    moles_units : dict
        Dictionary containing amounts of each mole unit per mol.

    """

    def get_time_units(self, year_conv: float) -> Dict[str, float]:
        """
        Get time units defined using floats.
        """

        return {
            "ps": 1.0e-12,
            "ns": 1.0e-9,
            "μs": 1.0e-6,
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
            "By": 86400.0 * year_conv * 1.0e9,
            "Gy": 86400.0 * year_conv * 1.0e9,
            "Ty": 86400.0 * year_conv * 1.0e12,
            "Py": 86400.0 * year_conv * 1.0e15,
        }

    def get_activity_units(self) -> Dict[str, float]:
        """
        Get activity units defined using floats.
        """

        return {
            "pBq": 1.0e-12,
            "nBq": 1.0e-9,
            "μBq": 1.0e-6,
            "uBq": 1.0e-6,
            "mBq": 1.0e-3,
            "Bq": 1.0,
            "kBq": 1.0e3,
            "MBq": 1.0e6,
            "GBq": 1.0e9,
            "TBq": 1.0e12,
            "PBq": 1.0e15,
            "EBq": 1.0e18,
            "pCi": 1.0e-12 * 3.7e10,
            "nCi": 1.0e-9 * 3.7e10,
            "μCi": 1.0e-6 * 3.7e10,
            "uCi": 1.0e-6 * 3.7e10,
            "mCi": 1.0e-3 * 3.7e10,
            "Ci": 1.0 * 3.7e10,
            "kCi": 1.0e3 * 3.7e10,
            "MCi": 1.0e6 * 3.7e10,
            "GCi": 1.0e9 * 3.7e10,
            "TCi": 1.0e12 * 3.7e10,
            "PCi": 1.0e15 * 3.7e10,
            "ECi": 1.0e18 * 3.7e10,
            "dpm": 60.0,
        }

    def get_mass_units(self) -> Dict[str, float]:
        """
        Get mass units defined using floats.
        """

        return {
            "pg": 1.0e-12,
            "ng": 1.0e-9,
            "μg": 1.0e-6,
            "ug": 1.0e-6,
            "mg": 1.0e-3,
            "g": 1.0,
            "kg": 1.0e3,
            "Mg": 1.0e6,
            "t": 1.0e6,
            "ton": 1.0e6,
        }

    def get_moles_units(self) -> Dict[str, float]:
        """
        Get moles units definted using floats.
        """

        return {
            "pmol": 1.0e-12,
            "nmol": 1.0e-9,
            "μmol": 1.0e-6,
            "umol": 1.0e-6,
            "mmol": 1.0e-3,
            "mol": 1.0,
            "kmol": 1.0e3,
            "Mmol": 1.0e6,
        }

    def __repr__(self) -> str:
        return f"UnitConverterFloat using {self.time_unit_conv(1, 'y', 'd')} days in a year."


class UnitConverterSympy(UnitConverter):
    """
    Unit converter using SymPy arbitrary precision operations.

    Parameters
    ----------
    year_conv : sympy.core.numbers.Rational
        Conversion factor for number of days in a year.

    Attributes
    ----------
    time_units : dict
        Dictionary containing numbers of each time unit per second.
    activity_units : dict
        Dictionary containing amounts of each activity unit per Bq.
    mass_units : dict
        Dictionary containing amounts of each mass unit per g.
    moles_units : dict
        Dictionary containing amounts of each mole unit per mol.

    """

    def get_time_units(self, year_conv: Rational) -> Dict[str, Expr]:
        """
        Get time units definted using Sympy Expressions.
        """

        return {
            "ps": Integer(1) / 1000000000000,
            "ns": Integer(1) / 1000000000,
            "μs": Integer(1) / 1000000,
            "us": Integer(1) / 1000000,
            "ms": Integer(1) / 1000,
            "s": Integer(1),
            "m": Integer(60),
            "h": Integer(3600),
            "d": Integer(86400),
            "y": Integer(86400) * year_conv,
            "sec": Integer(1),
            "second": Integer(1),
            "seconds": Integer(1),
            "hr": Integer(3600),
            "hour": Integer(3600),
            "hours": Integer(3600),
            "day": Integer(86400),
            "days": Integer(86400),
            "yr": Integer(86400) * year_conv,
            "year": Integer(86400) * year_conv,
            "years": Integer(86400) * year_conv,
            "ky": Integer(86400) * year_conv * 1000,
            "My": Integer(86400) * year_conv * 1000000,
            "By": Integer(86400) * year_conv * 1000000000,
            "Gy": Integer(86400) * year_conv * 1000000000,
            "Ty": Integer(86400) * year_conv * 1000000000000,
            "Py": Integer(86400) * year_conv * 1000000000000000,
        }

    def get_activity_units(self) -> Dict[str, Expr]:
        """
        Get activity units definted using Sympy Expressions.
        """

        return {
            "pBq": Integer(1) / 1000000000000,
            "nBq": Integer(1) / 1000000000,
            "μBq": Integer(1) / 1000000,
            "uBq": Integer(1) / 1000000,
            "mBq": Integer(1) / 1000,
            "Bq": Integer(1),
            "kBq": Integer(1000),
            "MBq": Integer(1000000),
            "GBq": Integer(1000000000),
            "TBq": Integer(1000000000000),
            "PBq": Integer(1000000000000000),
            "EBq": Integer(1000000000000000000),
            "pCi": Integer(1) / 1000000000000 * 37000000000,
            "nCi": Integer(1) / 1000000000 * 37000000000,
            "μCi": Integer(1) / 1000000 * 37000000000,
            "uCi": Integer(1) / 1000000 * 37000000000,
            "mCi": Integer(1) / 1000 * 37000000000,
            "Ci": Integer(1) * 37000000000,
            "kCi": Integer(1000) * 37000000000,
            "MCi": Integer(1000000) * 37000000000,
            "GCi": Integer(1000000000) * 37000000000,
            "TCi": Integer(1000000000000) * 37000000000,
            "PCi": Integer(1000000000000000) * 37000000000,
            "ECi": Integer(1000000000000000000) * 37000000000,
            "dpm": Integer(60),
        }

    def get_mass_units(self) -> Dict[str, Expr]:
        """
        Get mass units definted using Sympy Expressions.
        """

        return {
            "pg": Integer(1) / 1000000000000,
            "ng": Integer(1) / 1000000000,
            "μg": Integer(1) / 1000000,
            "ug": Integer(1) / 1000000,
            "mg": Integer(1) / 1000,
            "g": Integer(1),
            "kg": Integer(1000),
            "Mg": Integer(1000000),
            "t": Integer(1000000),
            "ton": Integer(1000000),
        }

    def get_moles_units(self) -> Dict[str, Expr]:
        """
        Get mole units definted using Sympy Expressions.
        """

        return {
            "pmol": Integer(1) / 1000000000000,
            "nmol": Integer(1) / 1000000000,
            "μmol": Integer(1) / 1000000,
            "umol": Integer(1) / 1000000,
            "mmol": Integer(1) / 1000,
            "mol": Integer(1),
            "kmol": Integer(1000),
            "Mmol": Integer(1000000),
        }

    def __repr__(self) -> str:
        return f"UnitConverterSympy using {self.time_unit_conv(1, 'y', 'd')} days in a year."


class QuantityConverter:
    """
    Converts activity in Bq, mass in g and moles in mol to number of atoms, and vice versa.
    Supports both Exprs or SymPy quantities.

    Parameters
    ----------
    atomic_masses : numpy.ndarray
        Column vector of the atomic masses (in g/mol).
    decay_consts : numpy.ndarray
        Column vector of the decay constants (in s\\ :sup:`-1`).
    nuclide_dict : dict
        Dictionary containing nuclide strings as keys and positions in the matrices as values.

    Attributes
    ----------
    atomic_masses : numpy.ndarray
        Column vector of the atomic masses (in g/mol).
    avogadro : float
        Avogadro constant (number of atoms/mol).
    decay_consts : numpy.ndarray
        Column vector of the decay constants (in s\\ :sup:`-1`).
    nuclide_dict : dict
        Dictionary containing nuclide strings as keys and positions in the matrices as values.

    """

    def __init__(
        self,
        nuclide_dict: Dict[str, int],
        atomic_masses: np.ndarray,
        decay_consts: np.ndarray,
    ) -> None:
        self.nuclide_dict = nuclide_dict
        self.atomic_masses = atomic_masses
        self.decay_consts = decay_consts
        self.avogadro = AVOGADRO

    def activity_to_number(
        self, nuclide: str, activity: Union[float, Expr]
    ) -> Union[float, Expr]:
        """
        Converts an activity in Bq to the number of atoms.

        Parameters
        ----------
        nuclide : str
            Nuclide string.
        activity : float or sympy.core.expr.Expr
            The activity in Bq of the nuclide to be converted.

        Returns
        -------
        float or sympy.core.expr.Expr
            Number of atoms of the nuclide.

        """

        return activity / self.decay_consts[self.nuclide_dict[nuclide]]

    def mass_to_number(
        self, nuclide: str, mass: Union[float, Expr]
    ) -> Union[float, Expr]:
        """
        Converts a mass in grams to number of atoms.

        Parameters
        ----------
        nuclide : str
            Nuclide string.
        mass : float or sympy.core.expr.Expr
            The mass of the nuclide to be converted in grams.

        Returns
        -------
        float or sympy.core.expr.Expr
            Number of atoms of the nuclide.

        """

        return mass / self.atomic_masses[self.nuclide_dict[nuclide]] * self.avogadro

    def moles_to_number(self, moles: Union[float, Expr]) -> Union[float, Expr]:
        """
        Converts number of moles to number of atoms.

        Parameters
        ----------
        moles : float or sympy.core.expr.Expr
            Number of moles to be converted.

        Returns
        -------
        float or sympy.core.expr.Expr
            Number of atoms.

        """

        return moles * self.avogadro

    def number_to_activity(
        self, nuclide: str, number: Union[float, Expr]
    ) -> Union[float, Expr]:
        """
        Converts number of atoms to activity in Bq.

        Parameters
        ----------
        nuclide : str
            Nuclide string.
        number : float or sympy.core.expr.Expr
            The number of atoms of nuclide to be converted.

        Returns
        -------
        float or sympy.core.expr.Expr
            Activity of the nuclide in Bq.

        """

        return number * self.decay_consts[self.nuclide_dict[nuclide]]

    def number_to_mass(
        self, nuclide: str, number: Union[float, Expr]
    ) -> Union[float, Expr]:
        """
        Converts number of atoms to mass in grams. Supports both Exprs or SymPy quantities.

        Parameters
        ----------
        nuclide : str
            Nuclide string.
        number : float or sympy.core.expr.Expr
            The number of atoms of the nuclide to be converted.

        Returns
        -------
        float or sympy.core.expr.Expr
            Mass of material in grams.

        """

        return number / self.avogadro * self.atomic_masses[self.nuclide_dict[nuclide]]

    def number_to_moles(self, number: Union[float, Expr]) -> Union[float, Expr]:
        """
        Converts number of atoms to moles of nuclide.

        Parameters
        ----------
        number : float or sympy.core.expr.Expr
            The number of atoms of the nuclide to be converted.

        Returns
        -------
        float or sympy.core.expr.Expr
            Moles of nuclide.

        """

        return number / self.avogadro

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``QuantityConverter`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, QuantityConverter):
            return NotImplemented
        return (
            (self.atomic_masses == other.atomic_masses).all()
            and self.avogadro == other.avogadro
            and (self.decay_consts == other.decay_consts).all()
            and self.nuclide_dict == other.nuclide_dict
        )

    def __ne__(self, other: object) -> bool:
        """
        Check whether two ``QuantityConverter`` instances are not equal with ``!=`` operator.
        """

        if not isinstance(other, QuantityConverter):
            return NotImplemented
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return "QuantityConverter using double-precision floats."


class QuantityConverterSympy(QuantityConverter):
    """
    Unit converter using SymPy arbitrary precision operations.

    Parameters
    ----------
    atomic_masses : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the atomic masses (in g/mol).
    decay_consts : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (in s\\ :sup:`-1`).
    nuclide_dict : dict
        Dictionary containing nuclide strings as keys and positions in the matrices as values.

    Attributes
    ----------
    atomic_masses : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the atomic masses (in g/mol).
    avogadro : sympy.core.numbers.Integer
        Avogadro constant (number of atoms/mol).
    decay_consts : sympy.matrices.dense.MutableDenseMatrix
        Column vector of the decay constants (in s\\ :sup:`-1`).
    nuclide_dict : dict
        Dictionary containing nuclide strings as keys and positions in the matrices as values.

    """

    def __init__(
        self,
        nuclide_dict: Dict[str, int],
        atomic_masses: Matrix,
        decay_consts: Matrix,
    ) -> None:
        super().__init__(nuclide_dict, atomic_masses, decay_consts)
        self.avogadro = nsimplify(self.avogadro)

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``QuantityConverterSympy`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, QuantityConverterSympy):
            return NotImplemented
        return (
            self.atomic_masses == other.atomic_masses
            and self.avogadro == other.avogadro
            and self.decay_consts == other.decay_consts
            and self.nuclide_dict == other.nuclide_dict
        )

    def __repr__(self) -> str:
        return "QuantityConverterSympy using SymPy arbitrary precision calculations."
