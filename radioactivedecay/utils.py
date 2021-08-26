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
        Dictionary containing nuclide strings or Radionuclide objects as keys and numbers
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
