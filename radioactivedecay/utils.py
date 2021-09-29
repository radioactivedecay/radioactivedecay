"""
The utils module contains functions to parse nuclide strings and manipulate lists and dictionaries.

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from typing import Dict, List, Union
from sympy.core.expr import Expr


Z_DICT = {
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    21: "Sc",
    22: "Ti",
    23: "V",
    24: "Cr",
    25: "Mn",
    26: "Fe",
    27: "Co",
    28: "Ni",
    29: "Cu",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    39: "Y",
    40: "Zr",
    41: "Nb",
    42: "Mo",
    43: "Tc",
    44: "Ru",
    45: "Rh",
    46: "Pd",
    47: "Ag",
    48: "Cd",
    49: "In",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
    54: "Xe",
    55: "Cs",
    56: "Ba",
    57: "La",
    58: "Ce",
    59: "Pr",
    60: "Nd",
    61: "Pm",
    62: "Sm",
    63: "Eu",
    64: "Gd",
    65: "Tb",
    66: "Dy",
    67: "Ho",
    68: "Er",
    69: "Tm",
    70: "Yb",
    71: "Lu",
    72: "Hf",
    73: "Ta",
    74: "W",
    75: "Re",
    76: "Os",
    77: "Ir",
    78: "Pt",
    79: "Au",
    80: "Hg",
    81: "Tl",
    82: "Pb",
    83: "Bi",
    84: "Po",
    85: "At",
    86: "Rn",
    87: "Fr",
    88: "Ra",
    89: "Ac",
    90: "Th",
    91: "Pa",
    92: "U",
    93: "Np",
    94: "Pu",
    95: "Am",
    96: "Cm",
    97: "Bk",
    98: "Cf",
    99: "Es",
    100: "Fm",
    101: "Md",
    102: "No",
    103: "Lr",
    104: "Rf",
    105: "Db",
    106: "Sg",
    107: "Bh",
    108: "Hs",
    109: "Mt",
    110: "Ds",
    111: "Rg",
    112: "Cn",
    113: "Nh",
    114: "Fl",
    115: "Mc",
    116: "Lv",
    117: "Ts",
    118: "Og",
}
SYM_DICT = dict((v, k) for k, v in Z_DICT.items())


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

    canonical_id = (Z * 10000000) + (A * 10000) + state_int

    return canonical_id


def build_nuclide_string(Z: int, A: int, meta_state: str = "") -> str:
    """
    Builds a nuclide string from given atomic mass and number.

    Parameters
    ----------
    Z : int
        Atomic number.
    A : int
        Atomic mass.
    meta_state : str, optional
        Metastable state indicator character, ex. 'm' for the first
        atomic metastable state.

    Returns
    -------
    str
        Nuclide string built in symbol - mass number format.

    Examples
    --------
    >>> rd.utils.build_nuclide_string(26, 56)
    'Fe-56'
    >>> rd.utils.build_nuclide_string(28, 56, 'm')
    'Fe-56m'

    """

    if Z not in Z_DICT.keys():
        raise ValueError(str(Z) + " is not a valid atomic number")

    return_string = Z_DICT[Z] + "-" + str(A) + meta_state

    return return_string


def parse_nuclide_str(nuclide: str) -> str:
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

    for idx in range(1, len(nuclide)):  # Add hyphen e.g. Tc99m to Tc-99m.
        if nuclide[idx].isdigit():
            if nuclide[idx - 1] != "-":
                nuclide = nuclide[:idx] + "-" + nuclide[idx:]
            break

    return nuclide


def parse_id(input_id: int) -> str:
    """
    Parses a nuclide canonical id in zzzaaammmm format into symbol -
    mass number format.

    Parameters
    ----------
    input_id : int
        Nuclide in canonical id format.

    Returns
    -------
    str
        Nuclide string parsed in symbol - mass number format.

    Examples
    --------
    >>> rd.utils.parse_id(190400000)
    'K-40'
    >>> rd.utils.parse_id(280560001)
    'Ni-56m'

    """

    id_zzzaaa = int(input_id / 10000)
    state_digits = input_id - (id_zzzaaa * 10000)
    state = ""
    if state_digits == 1:
        state = "m"
    elif state_digits == 2:
        state = "n"
    Z = int(id_zzzaaa / 1000)
    A = id_zzzaaa - (Z * 1000)
    name = build_nuclide_string(Z, A, state)

    return name


def parse_nuclide(
    input_nuclide: Union[str, int], nuclides: List[str], dataset_name: str
) -> str:
    """
    Parses a nuclide string or canonical id into symbol - mass number
    format and checks whether the nuclide is contained in the decay
    dataset.

    Parameters
    ----------
    input_nuclide : str or int
        Nuclide name string or canonical id in zzzaaammmm format.
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
        If the input nuclide string or id is invalid or the nuclide is
        not contained in the decay dataset.
    TypeError
        If the input is an invalid type, a string or integer is
        expected.

    Examples
    --------
    >>> rd.utils.parse_nuclide('222Rn', rd.DEFAULTDATA.nuclides, rd.DEFAULTDATA.dataset_name)
    'Rn-222'
    >>> rd.utils.parse_nuclide('Ba137m', rd.DEFAULTDATA.nuclides, rd.DEFAULTDATA.dataset_name)
    'Ba-137m'
    >>> rd.utils.parse_nuclide(280560001, rd.DEFAULTDATA.nuclides, rd.DEFAULTDATA.dataset_name)
    'Ni-56m'

    """

    original_input = input_nuclide
    if isinstance(input_nuclide, int):
        name = parse_id(input_nuclide)
    elif isinstance(input_nuclide, str):
        name = input_nuclide
    else:
        raise TypeError("Invalid input type, expected int or str")
    nuclide = parse_nuclide_str(name)

    if nuclide not in nuclides:
        raise ValueError(
            str(original_input)
            + " is not a valid nuclide in "
            + dataset_name
            + " decay dataset."
        )

    return nuclide


def add_dictionaries(
    dict_a: Dict[str, Union[float, Expr]], dict_b: Dict[str, Union[float, Expr]]
) -> Dict[str, Union[float, Expr]]:
    """
    Adds together two dictionaries of nuclide strings and associated quantities. Supports both
    floats or SymPy quantities.

    Parameters
    ----------
    dict_a : dict
        First dictionary containing nuclide strings as keys and quantitites as values.
    dict_b : dict
        Second dictionary containing nuclide strings as keys and quantitites as values.

    Returns
    -------
    dict
        Combined dictionary containing the nuclides in both dict_a and dict_b, where the
        quantities have been added together when a nuclide is present in both input
        dictionaries.

    Examples
    --------
    >>> dict_a = {'Pm-141': 1.0, 'Rb-78': 2.0}
    >>> dict_b = {'Pm-141': 3.0, 'Rb-90': 4.0}
    >>> rd.utils.add_dictionaries(dict_a, dict_b)
    {'Pm-141': 4.0, 'Rb-78': 2.0, 'Rb-90': 4.0}

    """

    new_dict = dict_a.copy()
    for nuclide, quantity in dict_b.items():
        if nuclide in new_dict:
            new_dict[nuclide] = new_dict[nuclide] + quantity
        else:
            new_dict[nuclide] = quantity

    return new_dict


def sort_dictionary_alphabetically(
    input_inv_dict: Dict[str, Union[float, Expr]]
) -> Dict[str, Union[float, Expr]]:
    """
    Sorts a dictionary alphabetically by its keys.

    Parameters
    ----------
    input_inv_dict : dict
        Dictionary containing nuclide strings or Nuclide objects as keys and numbers
        as values.

    Returns
    -------
    dict
        Inventory dictionary which has been sorted by the nuclides alphabetically.

    Examples
    --------
    >>> rd.utils.sort_dictionary_alphabetically({'U-235': 1.2, 'Tc-99m': 2.3, 'Tc-99': 5.8})
    {'Tc-99': 5.8, 'Tc-99m': 2.3, 'U-235': 1.2}

    """

    return dict(sorted(input_inv_dict.items(), key=lambda x: x[0]))


def sort_list_according_to_dataset(
    input_list: List[str], key_dict: Dict[str, int]
) -> List[str]:
    """
    Sorts a list of nuclides based on their order of appearence in the decay dataset.

    Parameters
    ----------
    input_list : list
        List of nuclide strings to be sorted.
    key_dict : dict
        Dictionary from the decay dataset with nuclide strings as keys and their position
        (integers) in the decay dataset.

    Returns
    -------
    list
        Sorted nuclide list.

    Examples
    --------
    >>> rd.utils.sort_list_according_to_dataset(['Tc-99', 'Tc-99m'], rd.DEFAULTDATA.nuclide_dict)
    ['Tc-99m', 'Tc-99']

    """

    return sorted(input_list, key=lambda nuclide: key_dict[nuclide])
