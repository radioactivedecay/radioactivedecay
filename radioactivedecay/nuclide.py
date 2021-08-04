"""
The nuclide module defines the ``Nuclide`` class. Each ``Nuclide``
instance represents one nuclide or element, and has a variety of ways
for contruction based off of a nuclide or element string, or atomic
number and mass. The class properties provide an easy way of
extracting atomic number and mass information, as well as a clean name
string.

The code examples shown in the docstrings assume the
``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

import os, csv
from typing import Any
from radioactivedecay.utils import parse_nuclide


class Nuclide:
    """
    ``Nuclide`` instances serve as name and atomic number/mass parsing
    objects for any nuclide or element.

    Parameters
    ----------
    input : Any
        Input value for instantiation. Can be nuclide string in name
        format (with or without hyphen), or atomic number (Z).
    A : int, optional
        For atomic number as input, atomic mass can be optionally
        added for full nuclide string construction. 

    Properties
    ----------
    name : str
        Nuclide string if A data is given, otherwise the element
        symbol is returned.
    Z : int
        Atomic number.
    A : int
        Atomic mass, returns 0 for raw elements.

    Examples
    --------
    >>> rd.Nuclide('K-40')
    Nuclide: K-40
    >>> rd.Nuclide('K40')
    Nuclide: K-40
    >>> rd.Nuclide('K')
    Element: K
    >>> rd.Nuclide(19, 40)
    Nuclide: K-40
    >>> rd.Nuclide(19)
    Element: K

    """
    
    def __init__(self, input: Any, A: int = 0) -> None:
        loc = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        sym_dict_path = os.path.join(loc, "element_symbols.csv")

        Z_dict, sym_dict = {}, {}
        with open(sym_dict_path, 'r') as f:
            csv_list = csv.DictReader(f)
            for row in csv_list:
                Z_dict[int(row["Z"])] = row["Symbol"]
                sym_dict[row["Symbol"]] = int(row["Z"])
        
        self.Z_dict = Z_dict
        self.sym_dict = sym_dict
        self.parse_name(input, A)

    def parse_name(self, vary_input: Any, A: int) -> None:
        if A == 0:
            if type(vary_input) == int:
                Z = vary_input
                name = self.build_nuclide_string(Z, A)
            elif type(vary_input) == str:
                if any(i in vary_input for i in ["0","1","2","3","4","5","6","7","8","9"]):
                    name = parse_nuclide(vary_input)
                    Z = self.sym_dict[name.split("-")[0]]
                    A = int(name.split("-")[1].strip("mn"))
                elif vary_input in self.Z_dict.values():
                    name = vary_input
                    Z = self.sym_dict[vary_input]
                else:
                    raise ValueError(
                        vary_input + ' is not a valid element or nuclide'
                    )
            else:
                raise TypeError(
                    "Invalid name input type, string or int expected"
                )
        elif type(vary_input) == int and type(A) == int:
            Z = vary_input
            name = self.build_nuclide_string(Z, A)
        else:
            raise TypeError(
                "Invalid input types, expected int"
            )
        
        self.nuclide_name = name
        self.Z_val = Z
        self.A_val = A
    
    def build_nuclide_string(self, Z: int, A: int = 0) -> str:            
        if Z not in self.Z_dict.keys():
            raise ValueError(
                str(Z) + ' is not a valid atomic number'
            )
            
        return_string = self.Z_dict[Z]
        if A != 0:
            return_string += "-" + str(A)
            
        return return_string
    
    def __repr__(self) -> str:
        if self.A == 0:
            rep =  "Element: " + self.name
        else:
            rep = "Nuclide: " + self.name
            
        return rep
    
    @property
    def name(self) -> str:
        """
        Returns the element or nuclide name of the object.

        Examples
        --------
        >>> rd.Nuclide("Fe-56").name
        Fe-56
        >>> rd.Nuclide("Fe56").name
        Fe-56
        >>> rd.Nuclide(26, 56).name
        Fe-56
        >>> rd.Nuclide("Fe").name
        Fe
        >>> rd.Nuclide(26).name
        Fe

        """
        return self.nuclide_name
    
    @property
    def Z(self) -> int:
        """
        Returns the atomic number of the element or nuclide.

        Examples
        --------
        >>> rd.Nuclide("Fe-56").Z
        26
        >>> rd.Nuclide("Fe56").Z
        26
        >>> rd.Nuclide(26, 56).Z
        26
        >>> rd.Nuclide("Fe").Z
        26
        >>> rd.Nuclide(26).Z
        26
        """
        
        return self.Z_val
    
    @property
    def A(self) -> int:
        """
        Returns the atomic mass of the nuclide, and 0 for elements.

        Examples
        --------
        >>> rd.Nuclide("Fe-56").A
        56
        >>> rd.Nuclide("Fe56").A
        56
        >>> rd.Nuclide(26, 56).A
        56
        >>> rd.Nuclide("Fe").A
        0
        >>> rd.Nuclide(26).A
        0
        """
        
        return self.A_val
        
