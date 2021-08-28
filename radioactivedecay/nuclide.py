"""
The nuclide module defines the ``Nuclide`` class. Each ``Nuclide``
instance represents one nuclide, and can be contructed from a nuclide
string or `zzzaaassss` canonical id. The class properties provide an
easy way of extracting atomic number and mass information, as well as a
clean name string. Furthermore, additional methods provide an access
point for mass data of nuclides, and the decay data of radionuclides,
if present in a specified dataset. The default decay dataset used if
none is supplied to the constructor is rd.DEFAULTDATA.

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
from radioactivedecay.utils import (
    parse_nuclide,
    elem_to_Z,
    build_id,
    build_nuclide_string
)


class Nuclide:
    """
    ``Nuclide`` instances serve as name and atomic number/mass parsing
    objects for any nuclide or element.

    Parameters
    ----------
    input : Any
        Input value for instantiation. Can be nuclide string in name
        format (with or without hyphen), or canonical id (zzzaaassss).

    Attributes
    ----------
    name : str
        Nuclide name string.
    Z : int
        Atomic number.
    A : int
        Atomic mass number.
    id : int
        Canonical nuclide id, in zzzaaassss form. Ground state is 0000,
        first excited state ("m") is 0001, second ("n") is 0002, etc.

    Examples
    --------
    >>> rd.Nuclide('K-40')
    Nuclide: K-40
    >>> rd.Nuclide('K40')
    Nuclide: K-40
    >>> rd.Nuclide(190400000)
    Nuclide: K-40
    >>> rd.Nuclide(280560001)
    Nuclide: Ni-56m

    """
    
    def __init__(
        self,
        input: Any,
        data: DecayData = DEFAULTDATA
    ) -> None:
        self.parse_name(input)
        self.data = data

    def parse_name(self, input: Any) -> None:
        if isinstance(input, int):
            self.id = input
            id_zzzaaa = int(input / 10000)
            state_digits = input - (id_zzzaaa * 10000)
            state = ""
            if state_digits == 1:
                state = "m"
            elif state_digits == 2:
                state = "n"
            Z = int(id_zzzaaa / 1000)
            A = id_zzzaaa - (Z * 1000)    
            name = build_nuclide_string(Z, A, state)
        elif isinstance(input, str):
            name = parse_nuclide(input)
            Z = elem_to_Z(name.split("-")[0])
            A = int(name.split("-")[1].strip("mn"))
            state = name.split("-")[1].strip("0123456789")
            self.id = build_id(Z, A, state)
        else:
            raise TypeError(
                "Invalid input type, expected int or str"
            )
        
        self.name = name
        self.Z = Z
        self.A = A
        self.state = state
    
    def __repr__(self) -> str:
        if self.A == 0:
            rep =  "Element: " + self.name
        else:
            rep = ("Nuclide: "
                   + self.name
                   + ", decay dataset: "
                   + self.data.dataset)
            
        return rep
    
    @property
    def atomic_mass(self) -> int:
        """
        Returns the atomic weight of the nuclide, if contained in the
        dataset.
        
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.

        Examples
        --------
        >>> Ir190n = rd.Nuclide('Ir-190n')
        >>> Ir190n.atomic_mass
        189.96094745600013
        
        """
        
        if self.name not in self.data.radionuclides:
            raise ValueError(
                self.name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        index = self.data.radionuclide_dict[self.name]
        mass = self.data.masses[index]
        return mass
    
    def half_life(self, units: str = "s") -> Union[float, str]:
        """
        Returns the half-life of a nuclide as a float in your chosen
        units, or as a human-readable string with appropriate units.

        Parameters
        ----------
        units : str, optional
            Units for half-life. Options are 'ps', 'ns', 'μs', 'us',
            'ms', 's', 'm', 'h', 'd', 'y', 'ky', 'My', 'By', 'Gy',
            'Ty', 'Py', and common spelling variations. Default is 's',
            i.e. seconds. Use 'readable' to get a string of the
            half-life in human-readable units.

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
        >>> Fe56 = rd.Nuclide('Fe-56')
        >>> Fe56.half_life('readable')
        'stable'

        """

        if self.name not in self.data.radionuclides:
            raise ValueError(
                self.name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        return self.data.half_life(self.name, units)

    @property
    def prog_bf_mode(self) -> Dict[str, List]:
        """
        Returns the direct progeny of a radionuclide.

        Returns
        -------
        prog_bf_mode : dict
            Dictionary containing direct progeny as keys, and a list
            containing the branching fraction and the decay mode for
            that progeny as values.
            
        Raises
        ------
        ValueError
            If the nuclide is not contained in the decay
            dataset.
            
        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.prog_bf_mode
        {'Ca-40': [0.8914, 'β-'], 'Ar-40': [0.1086, 'β+ & EC']}

        """
        
        if self.name not in self.data.radionuclides:
            raise ValueError(
                self.name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )
        
        return self.data.prog_bfs_modes[
            self.data.radionuclide_dict[self.name]
        ]
        
    def progeny(self) -> List[str]:
        """
        Returns the direct progeny of a radionuclide.

        Returns
        -------
        list
            List of the direct progeny of the radionuclide, ordered by
            decreasing branching fraction.
            
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
        Returns the branching fractions to the direct progeny of a
        radionuclide.

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
        Returns the decay modes for a radionuclide, as defined in the
        decay dataset. Note: the decay mode strings returned are not
        lists of all the different radiation types emitted during the
        parent to progeny decay processes. They are the labels defined
        in the decay dataset to classify the parent to progeny decay
        type (e.g. '\u03b1', '\u03b2-' or 'IT').

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

        if self.name not in self.data.radionuclides:
            raise ValueError(
                self.name
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
        Plots a diagram of the decay chain of a radionuclide. Then
        creates a NetworkX DiGraph and plot of it using NetworkX's
        Matplotlib-based plotting functionality.

        Some of the NetworkX default plotting parameters are changed to
        produce nice decay chain diagrams. However, users retain
        control over these parameters via kwargs_draw and
        kwargs_edge_labels. For more information on the various
        NetworkX plotting parameters, refer to its `documentation
        <https://networkx.org/documentation/stable/reference/drawing.html>`_.

        Parameters
        ----------
        label_pos : float, optional
            Position of labels along edges. Default is 0.5. If you find
            that edge labels are overlapping in the decay chain
            diagram, try increasing this parameter to e.g. 0.66.
        fig : None or matplotlib.figure.Figure, optional
            matplotlib figure object to use, or None makes
            ``radioactivedecay`` create one (default is None).
        ax : None or matplotlib.axes.Axes, optional
            matplotlib axes object to use, or None makes
            ``radioactivedecay`` create one (default is None).
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

        if self.name not in self.data.radionuclides:
            raise ValueError(
                self.name
                + " is not a valid radionuclide in "
                + self.data.dataset
                + " dataset."
            )

        digraph, max_generation, max_xpos = _build_decay_digraph(self,
                                                                 nx.DiGraph())

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
            G=digraph,
            pos=positions,
            ax=ax,
            labels=node_labels,
            **kwargs_draw,
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
        Check whether two ``Nuclide`` instances are equal with ``==``
        operator.
        """

        return self.name == other.name and self.data == other.data

    def __ne__(self, other) -> bool:
        """
        Check whether two ``Nuclide`` instances are not equal with
        ``!=`` operator.
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
        Maximum number of progeny within any one generation of the
        decay chain.

    """

    generation_max_xpos = {0: 0}

    parent = parent_rn.name
    dequeue = deque([parent])
    generations = deque([0])
    xpositions = deque([0])
    node_label = (
        _parse_nuclide_label(parent)
        + "\n"
        + str(parent_rn.half_life("readable"))
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
                    node_label += (
                        "\n"
                        + str(parent_rn.data.half_life(prog,
                                                       "readable"))
                    )
                    dequeue.append(prog)
                    generations.append(generation)
                    xpositions.append(xpos + xcounter)
                if prog == "SF":
                    prog = parent + "_SF"

                digraph.add_node(
                    prog,
                    generation=generation,
                    xpos=xpos + xcounter,
                    label=node_label
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

    return (digraph,
            max(generation_max_xpos),
            max(generation_max_xpos.values())