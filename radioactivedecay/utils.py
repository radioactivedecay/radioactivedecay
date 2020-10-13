"""
The utils module contains functions to parse nuclide strings, check the validity of inventory
dictionaries, convert between time units, add two dictionaries together.

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from functools import singledispatch, update_wrapper


def parse_nuclide(nuclide):
    """
    Parses a nuclide string from XXAb or AbXX format to Ab-XX format. Not this function works for
    both radioactive and stable nuclides.

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


def parse_radionuclide(radionuclide, radionuclides, dataset):
    """
    Parses a radionuclide string and checks whether the radionuclide is contained in the decay
    dataset.

    Parameters
    ----------
    radionuclide : str
        Radionuclide string.
    radionuclides : numpy.ndarray
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


def check_dictionary(inv_dict, radionuclides, dataset):
    """
    Checks validity of a dictionary of radionuclides and associated acitivities. Radionuclides
    must be in the decay dataset.

    Parameters
    ----------
    inv_dict : dict
        Dictionary containing radionuclide strings as keys and activities as values.
    radionuclides : numpy.ndarray
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
    >>> rd.utils.check_dictionary({'3H': 1.0}, rd.DEFAULTDATA.radionuclides, rd.DEFAULTDATA.dataset)
    {'H-3': 1.0}


    """

    inv_dict = {
        parse_radionuclide(nuc, radionuclides, dataset): act
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
    >>> rd.utils.time_unit_conv(1.0, 'd', 'h', rd.DEFAULTDATA.year_conv)
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
    """
    Adds together two dictionaries of radionuclies and associated acitivities.

    Parameters
    ----------
    dict1 : dict
        First dictionary containing radionuclide strings as keys and activities as values.
    dict2 : dict
        Second dictionary containing radionuclide strings as keys and activities as values.

    Returns
    -------
    dict
        Combined dictionary containing the radionuclides in both dict1 and dict2, where activities
        have been added together when a radionuclide is present in both input dictionaries.

    Examples
    --------
    >>> dict1 = {'Pm-141': 1.0, 'Rb-78': 2.0}
    >>> dict2 = {'Pm-141': 3.0, 'Rb-90': 4.0}
    >>> rd.utils.add_dictionaries(dict1, dict2)
    {'Pm-141': 4.0, 'Rb-78': 2.0, 'Rb-90': 4.0}

    """

    new_dict = dict1.copy()
    for radionuclide, radioactivity in dict2.items():
        if radionuclide in new_dict:
            new_dict[radionuclide] = new_dict[radionuclide] + radioactivity
        else:
            new_dict[radionuclide] = radioactivity

    return new_dict


def method_dispatch(func):
    """Adds singledispatch support for class methods."""

    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper
