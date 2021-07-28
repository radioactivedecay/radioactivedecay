"""
The utils module contains functions to parse nuclide strings and convert between time units.

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from typing import List
from sympy import Integer, Rational


def parse_nuclide_str(nuclide: str) -> str:
    """
    Parses a nuclide string from e.g. '241Pu' or 'Pu241' format to 'Pu-241' format. Not this
    function works for both radioactive and stable nuclides.

    Parameters
    ----------
    nuclide : str
        Nuclide string.

    Returns
    -------
    str
        Nuclide string parsed in symbol - mass number format.

    Examples
    --------
    >>> rd.utils.parse_nuclide_str('222Rn')
    'Rn-222'
    >>> rd.utils.parse_nuclide_str('Ca40')
    'Ca-40'

    """

    letter_flag, number_flag = False, False
    for char in nuclide:
        if char.isalpha():
            letter_flag = True
        if char.isdigit():
            number_flag = True
        if letter_flag and number_flag:
            break

    if not (letter_flag and number_flag) or len(nuclide) < 2 or len(nuclide) > 7:
        raise ValueError(str(nuclide) + " is not a valid nuclide string.")

    while nuclide[0].isdigit():  # Re-order inputs e.g. 99mTc to Tc99m.
        nuclide = nuclide[1:] + nuclide[0]
    if nuclide[0] in ["m", "n"]:
        nuclide = nuclide[1:] + nuclide[0]

    for i in range(1, len(nuclide)):  # Add hyphen e.g. Tc99m to Tc-99m.
        if nuclide[i].isdigit():
            if nuclide[i - 1] != "-":
                nuclide = nuclide[:i] + "-" + nuclide[i:]
            break

    return nuclide


def parse_nuclide(nuclide: str, nuclides: List[str], dataset_name: str) -> str:
    """
    Parses a nuclide string into symbol - mass number format and checks whether the
    nuclide is contained in the decay dataset.

    Parameters
    ----------
    nuclide : str
        Nuclide name string.
    nuclides : List[str]
        List of all the nuclides in the decay dataset.
    dataset_name : str
        Name of the decay dataset.

    Returns
    -------
    str
        Nuclide string parsed in symbol - mass number format.

    Raises
    ------
    ValueError
        If the input nuclide string is invalid or the nuclide is not contained in the decay
        dataset.

    Examples
    --------
    >>> rd.utils.parse_nuclide('222Rn', rd.DEFAULTDATA.nuclides, rd.DEFAULTDATA.dataset_name)
    'Rn-222'
    >>> rd.utils.parse_nuclide('Ba137m', rd.DEFAULTDATA.nuclides, rd.DEFAULTDATA.dataset_name)
    'Ba-137m'

    """

    original_nuclide = nuclide
    nuclide = parse_nuclide_str(nuclide)

    if nuclide not in nuclides:
        raise ValueError(
            str(original_nuclide)
            + " is not a valid nuclide in "
            + dataset_name
            + " decay dataset."
        )

    return nuclide


def time_unit_conv(
    time_period: float, units_from: str, units_to: str, year_conv: float
) -> float:
    """
    Converts a time period from one time unit to another.

    Parameters
    ----------
    time_period : float
        Time period before conversion.
    units_from : str
        Time unit before conversion
    units_to : str
        Time unit after conversion
    yeav_conv : float
        Conversion factor for number of days in a year.

    Returns
    -------
    float
        Time period in new units.

    Raises
    ------
    ValueError
        If one of the time unit parameters is invalid.

    Examples
    --------
    >>> rd.utils.time_unit_conv(1.0, 'd', 'h', rd.DEFAULTDATA.year_conv)
    24.0

    """

    conv = {
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

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )

    return time_period * conv[units_from] / conv[units_to]


def time_unit_conv_sympy(
    time_period: Rational, units_from: str, units_to: str, year_conv: Rational
) -> Rational:
    """
    Same functionality as time_unit_conv(), but uses SymPy arbitrary-precision arithmetic.

    Parameters
    ----------
    time_period : sympy.core.numbers.Rational
        Time period before conversion.
    units_from : str
        Time unit before conversion
    units_to : str
        Time unit after conversion
    yeav_conv : sympy.core.numbers.Rational
        Conversion factor for number of days in a year.

    Returns
    -------
    sympy.core.numbers.Rational
        Time period in new units.

    Raises
    ------
    ValueError
        If one of the time unit parameters is invalid.

    """

    conv = {
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

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".'
        )

    return time_period * conv[units_from] / conv[units_to]


def activity_unit_conv(activity: float, units_from: str, units_to: str) -> float:
    """
    Converts an activity from one unit to another.

    Parameters
    ----------
    activity : float
        Activity before conversion.
    units_from : str
        Activity unit before conversion
    units_to : str
        Activity unit after conversion

    Returns
    -------
    float
        Activity in new units.

    Raises
    ------
    ValueError
        If one of the activity unit parameters is invalid.

    Examples
    --------
    >>> rd.utils.activity_unit_conv(1.0, 'Ci', 'Bq')
    3.7e10

    """

    curie_to_Bq = 3.7e10

    conv = {
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
        "pCi": 1.0e-12 * curie_to_Bq,
        "nCi": 1.0e-9 * curie_to_Bq,
        "μCi": 1.0e-6 * curie_to_Bq,
        "uCi": 1.0e-6 * curie_to_Bq,
        "mCi": 1.0e-3 * curie_to_Bq,
        "Ci": 1.0 * curie_to_Bq,
        "kCi": 1.0e3 * curie_to_Bq,
        "MCi": 1.0e6 * curie_to_Bq,
        "GCi": 1.0e9 * curie_to_Bq,
        "TCi": 1.0e12 * curie_to_Bq,
        "PCi": 1.0e15 * curie_to_Bq,
        "ECi": 1.0e18 * curie_to_Bq,
        "dpm": 60.0,
    }

    if units_from not in conv:
        raise ValueError(
            str(units_from)
            + ' is not a valid activitiy unit, e.g. "Bq", "kBq", "Ci"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a activitiy unit, e.g. "Bq", "kBq", "Ci"...'
        )

    return activity * conv[units_from] / conv[units_to]


def activity_unit_conv_sympy(
    activity: Rational, units_from: str, units_to: str
) -> Rational:
    """
    Same functionality as activity_unit_conv(), but uses SymPy arbitrary-precision arithmetic.

    Parameters
    ----------
    activity : sympy.core.numbers.Rational
        Activity before conversion.
    units_from : str
        Activity unit before conversion
    units_to : str
        Activity unit after conversion

    Returns
    -------
    sympy.core.numbers.Rational
        Activity in new units.

    Raises
    ------
    ValueError
        If one of the activity unit parameters is invalid.

    """

    curie_to_Bq = 37000000000

    conv = {
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
        "pCi": Integer(1) / 1000000000000 * curie_to_Bq,
        "nCi": Integer(1) / 1000000000 * curie_to_Bq,
        "μCi": Integer(1) / 1000000 * curie_to_Bq,
        "uCi": Integer(1) / 1000000 * curie_to_Bq,
        "mCi": Integer(1) / 1000 * curie_to_Bq,
        "Ci": Integer(1) * curie_to_Bq,
        "kCi": Integer(1000) * curie_to_Bq,
        "MCi": Integer(1000000) * curie_to_Bq,
        "GCi": Integer(1000000000) * curie_to_Bq,
        "TCi": Integer(1000000000000) * curie_to_Bq,
        "PCi": Integer(1000000000000000) * curie_to_Bq,
        "ECi": Integer(1000000000000000000) * curie_to_Bq,
        "dpm": Integer(60),
    }

    if units_from not in conv:
        raise ValueError(
            str(units_from)
            + ' is not a valid activitiy unit, e.g. "Bq", "kBq", "Ci"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid activitiy unit, e.g. "Bq", "kBq", "Ci"...'
        )

    return activity * conv[units_from] / conv[units_to]


def mass_unit_conv(mass: float, units_from: str, units_to: str) -> float:
    """
    Converts a mass from one unit to another.

    Parameters
    ----------
    mass : float
        Mass before conversion.
    units_from : str
        Mass unit before conversion
    units_to : str
        Mass unit after conversion

    Returns
    -------
    float
        Mass in new units.

    Raises
    ------
    ValueError
        If one of the mass unit parameters is invalid.

    Examples
    --------
    >>> rd.utils.mass_unit_conv(1.0, 'Ci', 'Bq')
    3.7e10

    """

    conv = {
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

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
        )

    return mass * conv[units_from] / conv[units_to]


def mass_unit_conv_sympy(mass: Rational, units_from: str, units_to: str) -> Rational:
    """
    Same functionality as mass_unit_conv(), but uses SymPy arbitrary-precision arithmetic.

    Parameters
    ----------
    mass : sympy.core.numbers.Rational
        Mass before conversion.
    units_from : str
        Mass unit before conversion
    units_to : str
        Mass unit after conversion

    Returns
    -------
    sympy.core.numbers.Rational
        Mass in new units.

    Raises
    ------
    ValueError
        If one of the mass unit parameters is invalid.

    """

    conv = {
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

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid mass unit, e.g. "g", "kg", "mg"...'
        )

    return mass * conv[units_from] / conv[units_to]


def moles_unit_conv(moles: float, units_from: str, units_to: str) -> float:
    """
    Converts a number of moles from one order of magnitude to another.

    Parameters
    ----------
    moles : float
        Amount before conversion.
    units_from : str
        Unit before conversion.
    units_to : str
        Unit after conversion.

    Returns
    -------
    float
        Result in chosen units.

    Raises
    ------
    ValueError
        If one of the unit parameters is invalid.

    Examples
    --------
    >>> rd.utils.moles_unit_conv(1.0, 'Ci', 'Bq')
    3.7e10

    """

    conv = {
        "pmol": 1.0e-12,
        "nmol": 1.0e-9,
        "μmol": 1.0e-6,
        "umol": 1.0e-6,
        "mmol": 1.0e-3,
        "mol": 1.0,
        "kmol": 1.0e3,
        "Mmol": 1.0e6,
    }

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
        )

    return moles * conv[units_from] / conv[units_to]


def moles_unit_conv_sympy(moles: Rational, units_from: str, units_to: str) -> Rational:
    """
    Same functionality as mass_unit_conv(), but uses SymPy arbitrary-precision arithmetic.

    Parameters
    ----------
    moles : sympy.core.numbers.Rational
        Amount before conversion.
    units_from : str
        Unit before conversion.
    units_to : str
        Unit after conversion.

    Returns
    -------
    sympy.core.numbers.Rational
        Result in chosen units.

    Raises
    ------
    ValueError
        If one of the unit parameters is invalid.

    """

    conv = {
        "pmol": Integer(1) / 1000000000000,
        "nmol": Integer(1) / 1000000000,
        "μmol": Integer(1) / 1000000,
        "umol": Integer(1) / 1000000,
        "mmol": Integer(1) / 1000,
        "mol": Integer(1),
        "kmol": Integer(1000),
        "Mmol": Integer(1000000),
    }

    if units_from not in conv:
        raise ValueError(
            str(units_from) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
        )
    if units_to not in conv:
        raise ValueError(
            str(units_to) + ' is not a valid unit, e.g. "mol", "kmol", "mmol"...'
        )

    return moles * conv[units_from] / conv[units_to]
