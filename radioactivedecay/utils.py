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


Z_DICT = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
    9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti",
    23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
    30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr",
    37: "Rb", 38: "Sr", 39: "Y", 40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc",
    44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La",
    58: "Ce", 59: "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd",
    65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb", 71: "Lu",
    72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt",
    79: "Au", 80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At",
    86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th", 91: "Pa", 92: "U",
    93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",
    100: "Fm", 101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db",
    106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds", 111: "Rg",
    112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts",
    118: "Og"
}
SYM_DICT = dict((v,k) for k,v in Z_DICT.items())



def Z_to_elem(Z: int) -> str:
    """
    Converts atomic number to element symbol.

    Parameters
    ----------
    Z : int
        Atomic number.

    Returns
    -------
    str
        Element string.

    Examples
    --------
    >>> rd.utils.Z_to_elem(1)
    'H'
    >>> rd.utils.Z_to_elem(35)
    'Br'

    """
        
    return Z_DICT[Z]


def elem_to_Z(sym: str) -> int:
    """
    Converts element symbol to atomic number.

    Parameters
    ----------
    sym : str
        Element string.

    Returns
    -------
    int
        Atomic number.

    Examples
    --------
    >>> rd.utils.elem_to_Z('H')
    1
    >>> rd.utils.elem_to_Z('Br')
    35

    """
            
    return SYM_DICT[sym]


def build_id(Z: int, A: int, state: str = "") -> int:
    """
    Builds a canonical nuclide id from atomic number, atomic mass, and
    and energy state.

    Parameters
    ----------
    Z : int
        Atomic number.
    A : int
        Atomic mass.
    state : str
        energy state.

    Returns
    -------
    int
        Canonical nuclide id.

    Examples
    --------
    >>> rd.utils.build_id(1,2)
    10020000
    >>> rd.utils.build_id(28,56,'m')
    280560001

    """
    
    if state != "":
        if state == "m":
            state_int = 1
        elif state == "n":
            state_int = 2
        else:
            raise ValueError(state + " is not a valid energy state.")
    else:
        state_int = 0
    
    id = (Z * 10000000) + (A * 10000) + state_int

    return id
                  

def build_nuclide_string(
    Z: int,
    A: int,
    meta_state: str = ""
) -> str:
                
    if Z not in Z_DICT.keys():
        raise ValueError(
            str(Z) + ' is not a valid atomic number'
        )
        
    return_string = Z_DICT[Z] + "-" + str(A) + meta_state
        
    return return_string


def parse_nuclide(nuclide: str) -> str:
    """
    Parses a nuclide string from e.g. '241Pu' or 'Pu241' format to 'Pu-241' format. Note this
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
    >>> rd.utils.parse_nuclide('222Rn')
    'Rn-222'
    >>> rd.utils.parse_nuclide('Ca40')
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


def parse_radionuclide(
    radionuclide: str, radionuclides: List[str], dataset: str
) -> str:
    """
    Parses a radionuclide string into symbol - mass number format and checks whether the
    radionuclide is contained in the decay dataset.

    Parameters
    ----------
    radionuclide : str
        Radionuclide string.
    radionuclides : List[str]
        List of all the radionuclides in the decay dataset.
    dataset : str
        Name of the decay dataset.

    Returns
    -------
    str
        Radionuclide string parsed in symbol - mass number format.

    Raises
    ------
    ValueError
        If the radionuclide string is invalid or the radionuclide is not contained in the decay
        dataset.

    Examples
    --------
    >>> rd.utils.parse_radionuclide('222Rn', rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    'Rn-222'
    >>> rd.utils.parse_radionuclide('Ba137m', rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    'Ba-137m'

    """

    original_radionuclide = radionuclide
    radionuclide = parse_nuclide(radionuclide)

    if radionuclide not in radionuclides:
        raise ValueError(
            str(original_radionuclide)
            + " is not a valid radionuclide in "
            + dataset
            + " dataset."
        )

    return radionuclide


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
