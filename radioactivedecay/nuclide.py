"""
The nuclide module defines the ``Nuclide`` class. Each ``Nuclide``
instance represents one nuclide or element, and has a variety of ways
for contruction based off of a nuclide or element string, atomic
number and mass, or `zzzaaassss` canonical id. The class properties
provide an easy way of extracting atomic number and mass information,
as well as a clean name string. Furthermore, additional methods provide
an access point for mass data of nuclides, and the decay data of
radionuclides, if present in a specified dataset. The default decay
dataset used if none is supplied to the constructor is rd.DEFAULTDATA.

The code examples shown in the docstrings assume the
``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from collections import deque
from typing import Any, Dict, List, Tuple, Union
import matplotlib
import networkx as nx
from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.plots import (
    _parse_nuclide_label,
    _parse_decay_mode_label,
    _check_fig_ax,
)
from radioactivedecay.utils import parse_radionuclide
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
    
    def __init__(
        self, input: Any,
        A: int = 0,
        meta_state: str = "",
        data: DecayData = DEFAULTDATA
        ) -> None:
        
        Z_dict = {
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
        sym_dict = dict((v,k) for k,v in Z_dict.items())
        
        self.Z_dict = Z_dict
        self.sym_dict = sym_dict
        self.parse_name(input, A, meta_state)
        self.data = data

    def parse_name(
        self,
        vary_input: Any,
        A: int,
        meta_state: str
        ) -> None:
        
        if A == 0:
            if type(vary_input) == int:
                if vary_input > 10000000:
                    id_zzzaaa = int(vary_input / 10000)
                    state_digits = vary_input - (id_zzzaaa * 10000)
                    if state_digits == 1:
                        meta_state = "m"
                    elif state_digits == 2:
                        meta_state = "n"
                    Z = int(id_zzzaaa / 1000)
                    A = id_zzzaaa - (Z * 1000)
                else:
                    Z = vary_input
                
                name = self.build_nuclide_string(Z, A, meta_state)
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
    
    def build_nuclide_string(
        self,
        Z: int,
        A: int = 0,
        meta_state: str = ""
        ) -> str:
                    
        if Z not in self.Z_dict.keys():
            raise ValueError(
                str(Z) + ' is not a valid atomic number'
            )
            
        return_string = self.Z_dict[Z]
        if A != 0:
            return_string += "-" + str(A) + meta_state
            
        return return_string
    
    def __repr__(self) -> str:
        if self.A == 0:
            rep =  "Element: " + self.nuclide_name
        else:
            rep = "Nuclide: " + self.nuclide_name + ", decay dataset: " + self.data.dataset
            
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
    
    @property
    def atomic_mass(self) -> int:
        """
        Returns the atomic mass of the nuclide, if contained in the dataset.
        
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Examples
        --------
        >>> rd.Nuclide("Fe-56").atomic_mass
        56
        >>> rd.Nuclide("Fe56").atomic_mass
        56
        >>> rd.Nuclide(26, 56).atomic_mass
        56
        """
        
        if self.nuclide_name not in self.data.radionuclides:
            raise ValueError(
                self.nuclide_name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        index = self.data.radionuclide_dict[self.nuclide_name]
        mass = self.data.masses[index]
        return mass
    
    def half_life(self, units: str = "s") -> Union[float, str]:
        """
        Returns the half-life of a radionuclide as a float in your chosen units, or as
        a human-readable string with appropriate units.

        Parameters
        ----------
        units : str, optional
            Units for half-life. Options are 'ps', 'ns', 'μs', 'us', 'ms', 's', 'm', 'h', 'd', 'y',
            'ky', 'My', 'By', 'Gy', 'Ty', 'Py', and common spelling variations. Default is 's', i.e.
            seconds. Use 'readable' to get a string of the half-life in human-readable units.

        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Returns
        -------
        float or str
            Radionuclide half-life.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.half_life('y')
        1251000000.0

        """

        if self.nuclide_name not in self.data.radionuclides:
            raise ValueError(
                self.nuclide_name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        return self.data.half_life(self.nuclide_name, units)

    @property
    def prog_bf_mode(self) -> Dict[str, List]:
        """
        Returns the direct progeny of a radionuclide.

        Returns
        -------
        prog_bf_mode : dict
            Dictionary containing direct progeny as keys, and a list containing the branching fraction
            and the decay mode for that progeny as values.
            
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        """
        
        if self.nuclide_name not in self.data.radionuclides:
            raise ValueError(
                self.nuclide_name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        return self.data.prog_bfs_modes[
            self.data.radionuclide_dict[self.nuclide_name]
        ]
        
    def progeny(self) -> List[str]:
        """
        Returns the direct progeny of a radionuclide.

        Returns
        -------
        list
            List of the direct progeny of the radionuclide, ordered by decreasing branching
            fraction.
            
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.progeny()
        ['Ca-40', 'Ar-40']

        """

        return list(self.prog_bf_mode.keys())

    def branching_fractions(self) -> List[float]:
        """
        Returns the branching fractions to the direct progeny of a radionuclide.

        Returns
        -------
        list
            List of branching fractions.
            
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.branching_fractions()
        [0.8914, 0.1086]

        """
            
        return [bf_mode[0] for bf_mode in list(self.prog_bf_mode.values())]

    def decay_modes(self) -> List[str]:
        """
        Returns the decay modes for a radionuclide, as defined in the decay dataset. Note: the
        decay mode strings returned are not lists of all the different radiation types emitted
        during the parent to progeny decay processes. They are the labels defined in the decay
        dataset to classify the parent to progeny decay type (e.g. '\u03b1', '\u03b2-' or 'IT').

        Returns
        -------
        list
            List of decay modes.
                
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.decay_modes()
        ['\u03b2-', '\u03b2+ & EC']

        """

        if self.nuclide_name not in self.data.radionuclides:
            raise ValueError(
                self.nuclide_name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
            
        return [bf_mode[1] for bf_mode in list(self.prog_bf_mode.values())]

    def plot(
        self,
        label_pos: float = 0.5,
        fig: Union[None, matplotlib.figure.Figure] = None,
        ax: Union[None, matplotlib.axes.Axes] = None,
        kwargs_draw: Union[None, Dict[str, Any]] = None,
        kwargs_edge_labels: Union[None, Dict[str, Any]] = None,
    ) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
        """
        Plots a diagram of the decay chain of a radionuclide. The creates a NetworkX DiGraph and
        creates a plot of it using NetworkX's Matplotlib-based plotting functionality.

        Some of the NetworkX default plotting parameters are changed to produce nice decay chain
        diagrams. However, users retain control over these parameters via kwargs_draw and
        kwargs_edge_labels. For more information on the various NetworkX plotting parameters,
        refer to its `documentation
        <https://networkx.org/documentation/stable/reference/drawing.html>`_.

        Parameters
        ----------
        label_pos : float, optional
            Position of labels along edges. Default is 0.5. If you find that edge labels are
            overlapping in the decay chain diagram, try increasing this parameter to e.g. 0.66.
        fig : None or matplotlib.figure.Figure, optional
            matplotlib figure object to use, or None makes ``radioactivedecay`` create one (default
            is None).
        ax : None or matplotlib.axes.Axes, optional
            matplotlib axes object to use, or None makes ``radioactivedecay`` create one (default
            is None).
        **kwargs_draw, optional
            Keyword arguments for networkx.draw().
        **kwargs_edge_labels, optional
            Keyword arguments for networkx.draw_networkx_edge_labels().

        Returns
        -------
        fig : matplotlib.figure.Figure
            matplotlib figure object used to plot the decay chain.
        ax : matplotlib.axes.Axes
            matplotlib axes object used to plot the decay chain.
                
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        """

        if self.nuclide_name not in self.data.radionuclides:
            raise ValueError(
                self.nuclide_name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )

        digraph, max_generation, max_xpos = _build_decay_digraph(self, nx.DiGraph())

        positions = nx.get_node_attributes(digraph, "pos")
        node_labels = nx.get_node_attributes(digraph, "label")
        edge_labels = nx.get_edge_attributes(digraph, "label")

        fig, ax = _check_fig_ax(
            fig, ax, figsize=(3 * max_xpos + 1.5, 3 * max_generation + 1.5)
        )

        if kwargs_draw is None:
            kwargs_draw = {}
        if "node_size" not in kwargs_draw:
            kwargs_draw["node_size"] = 6000
        if "node_color" not in kwargs_draw:
            kwargs_draw["node_color"] = "#FFFFFF"
        if "edgecolors" not in kwargs_draw:
            kwargs_draw["edgecolors"] = "#000000"

        nx.draw(
            G=digraph, pos=positions, ax=ax, labels=node_labels, **kwargs_draw,
        )

        if kwargs_edge_labels is None:
            kwargs_edge_labels = {}
        if "font_size" not in kwargs_edge_labels:
            kwargs_edge_labels["font_size"] = 12
        if "bbox" not in kwargs_edge_labels:
            kwargs_edge_labels["bbox"] = dict(
                boxstyle=None, ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)
            )
        if "rotate" not in kwargs_edge_labels:
            kwargs_edge_labels["rotate"] = False

        nx.draw_networkx_edge_labels(
            G=digraph,
            pos=positions,
            edge_labels=edge_labels,
            label_pos=label_pos,
            ax=ax,
            **kwargs_edge_labels,
        )

        ax.set_xlim(-0.3, max_xpos + 0.3)
        ax.set_ylim(-max_generation - 0.3, 0.3)

        return fig, ax

    def __eq__(self, other) -> bool:
        """
        Check whether two ``Nuclide`` instances are equal with ``==`` operator.
        """

        return self.nuclide_name == other.nuclide_name and self.data == other.data

    def __ne__(self, other) -> bool:
        """
        Check whether two ``Nuclide`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Hash function for ``Nuclide`` instances.
        """

        return hash((self.nuclide, self.data.dataset))


def _build_decay_digraph(
    parent_rn: Nuclide, digraph=nx.classes.digraph.DiGraph,
) -> nx.classes.digraph.DiGraph:
    """
    Build a networkx DiGraph for the decay chain of this radionuclide.

    Parameters
    ----------
    parent_rn : Nuclide
        Nuclide instance of the parent radionuclide of the decay chain.
    digraph : networkx.classes.digraph.DiGraph
        DiGraph for the decay chain.

    Returns
    -------
    digraph : networkx.classes.digraph.DiGraph
        DiGraph of the decay chain.
    max_generation : int
        Number of generations of progeny in the decay chain.
    max_xpos : int
        Maximum number of progeny within any one generation of the decay chain.

    """

    generation_max_xpos = {0: 0}

    parent = parent_rn.nuclide_name
    dequeue = deque([parent])
    generations = deque([0])
    xpositions = deque([0])
    node_label = (
        _parse_nuclide_label(parent) + "\n" + str(parent_rn.half_life("readable"))
    )
    digraph.add_node(parent, generation=0, xpos=0, label=node_label)
    seen = {parent}

    while len(dequeue) > 0:
        parent = dequeue.popleft()
        generation = generations.popleft() + 1
        xpos = xpositions.popleft()
        if generation not in generation_max_xpos:
            generation_max_xpos[generation] = -1
        parent_rn = Nuclide(parent, data=parent_rn.data)

        progeny = parent_rn.progeny()
        branching_fractions = parent_rn.branching_fractions()
        decay_modes = parent_rn.decay_modes()

        if xpos < generation_max_xpos[generation] + 1:
            xpos = generation_max_xpos[generation] + 1
        xcounter = 0
        for i, prog in enumerate(progeny):
            if prog not in seen:
                node_label = _parse_nuclide_label(prog)
                if prog in parent_rn.data.radionuclide_dict:
                    node_label += "\n" + str(parent_rn.data.half_life(prog, "readable"))
                    dequeue.append(prog)
                    generations.append(generation)
                    xpositions.append(xpos + xcounter)
                if prog == "SF":
                    prog = parent + "_SF"

                digraph.add_node(
                    prog, generation=generation, xpos=xpos + xcounter, label=node_label,
                )
                seen.add(prog)

                if xpos + xcounter > generation_max_xpos[generation]:
                    generation_max_xpos[generation] = xpos + xcounter
                xcounter += 1

            edge_label = (
                _parse_decay_mode_label(decay_modes[i])
                + "\n"
                + str(branching_fractions[i])
            )
            digraph.add_edge(parent, prog, label=edge_label)

    for node in digraph:
        digraph.nodes[node]["pos"] = (
            digraph.nodes[node]["xpos"],
            digraph.nodes[node]["generation"] * -1,
        )

    return digraph, max(generation_max_xpos), max(generation_max_xpos.values())