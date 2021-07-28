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
