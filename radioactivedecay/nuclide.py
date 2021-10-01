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
from typing import Any, Dict, List, Optional, Tuple, Union
import matplotlib
import networkx as nx
import numpy as np
from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.plots import (
    _parse_nuclide_label,
    _parse_decay_mode_label,
    _check_fig_axes,
)
from radioactivedecay.utils import parse_nuclide, elem_to_Z, build_id


class Nuclide:
    """
    ``Nuclide`` instances serve as name and atomic number/mass parsing
    objects for any nuclide or element.

    Parameters
    ----------
    input_nuclide : str or int
        Input value for instantiation. Can be nuclide string in name
        format (with or without hyphen), or canonical id (zzzaaassss).
    decay_data : DecayData, optional
        Decay dataset (default is the ICRP-107 dataset).

    Attributes
    ----------
    nuclide: str
        Nuclide name string.
    Z : int
        Atomic number.
    A : int
        Atomic mass number.
    id : int
        Canonical nuclide id, in zzzaaassss form. Ground state is 0000,
        first excited state ("m") is 0001, second ("n") is 0002, etc.
    decay_data : DecayData
        Decay dataset.
    atomic_mass : float
        Atomic weight of the nuclide, in g/mol.
    prog : list
        List of direct progeny of this nuclide.
    bfs : list
        List of branching fractions to direct progeny of this nuclide.
    modes : list
        List of modes to direct progeny of this nuclide.

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
        self, input_nuclide: Union[str, int], decay_data: DecayData = DEFAULTDATA
    ) -> None:
        self.decay_data = decay_data
        self.parse_name(input_nuclide)
        idx = decay_data.nuclide_dict[self.nuclide]
        self.atomic_mass = decay_data.scipy_data.atomic_masses[idx]
        self.prog: List[str] = decay_data.progeny[idx]
        self.bfs: List[float] = decay_data.bfs[idx]
        self.modes: List[str] = decay_data.modes[idx]

    def parse_name(self, input_nuclide: Union[str, int]) -> None:
        """
        Parse input and set atomic data attributes.
        """

        self.nuclide = parse_nuclide(
            input_nuclide, self.decay_data.nuclides, self.decay_data.dataset_name
        )
        self.Z = elem_to_Z(self.nuclide.split("-")[0])
        self.A = int(self.nuclide.split("-")[1].strip("mn"))
        self.state = self.nuclide.split("-")[1].strip("0123456789")
        self.id = build_id(self.Z, self.A, self.state)

    def __repr__(self) -> str:
        rep = (
            "Nuclide: "
            + self.nuclide
            + ", decay dataset: "
            + self.decay_data.dataset_name
        )

        return rep

    def __eq__(self, other: object) -> bool:
        """
        Check whether two ``Radionuclide`` instances are equal with ``==`` operator.
        """

        if not isinstance(other, Nuclide):
            return NotImplemented
        return self.nuclide == other.nuclide and self.decay_data == other.decay_data

    def __ne__(self, other: object) -> bool:
        """
        Check whether two ``Radionuclide`` instances are not equal with ``!=`` operator.
        """

        if not isinstance(other, Nuclide):
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Hash function for ``Radionuclide`` instances.
        """

        return hash((self.nuclide, self.decay_data.dataset_name))

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

        return self.decay_data.half_life(self.nuclide, units)

    def progeny(self) -> List[str]:
        """
        Returns the direct progeny of a radionuclide.

        Returns
        -------
        list
            List of the direct progeny of the radionuclide, ordered by
            decreasing branching fraction.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.progeny()
        ['Ca-40', 'Ar-40']

        """

        return self.prog

    def branching_fractions(self) -> List[float]:
        """
        Returns the branching fractions to the direct progeny of a
        radionuclide.

        Returns
        -------
        list
            List of branching fractions.

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.branching_fractions()
        [0.8914, 0.1086]

        """

        return self.bfs

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

        Examples
        --------
        >>> K40 = rd.Nuclide('K-40')
        >>> K40.decay_modes()
        ['\u03b2-', '\u03b2+ & EC']

        """

        return self.modes

    def plot(
        self,
        label_pos: float = 0.5,
        fig: Optional[matplotlib.figure.Figure] = None,
        axes: Optional[matplotlib.axes.Axes] = None,
        kwargs_draw: Optional[Dict[str, Any]] = None,
        kwargs_edge_labels: Optional[Dict[str, Any]] = None,
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
        axes : None or matplotlib.axes.Axes, optional
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

        """

        digraph, max_generation, max_xpos = _build_decay_digraph(self, nx.DiGraph())

        positions = nx.get_node_attributes(digraph, "pos")
        node_labels = nx.get_node_attributes(digraph, "label")
        edge_labels = nx.get_edge_attributes(digraph, "label")

        fig, axes = _check_fig_axes(
            fig, axes, figsize=(3 * max_xpos + 1.5, 3 * max_generation + 1.5)
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
            ax=axes,
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
            ax=axes,
            **kwargs_edge_labels,
        )

        axes.set_xlim(-0.3, max_xpos + 0.3)
        axes.set_ylim(-max_generation - 0.3, 0.3)

        return fig, axes


def _build_decay_digraph(
    parent: Nuclide,
    digraph: nx.classes.digraph.DiGraph,
) -> nx.classes.digraph.DiGraph:
    """
    Build a networkx DiGraph for the decay chain of this nuclide.

    Parameters
    ----------
    parent : Radionuclide
        Radionuclide instance of the parent nuclide of the decay chain.
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

    dequeue = deque([parent.nuclide])
    generations = deque([0])
    xpositions = deque([0])
    node_label = (
        _parse_nuclide_label(parent.nuclide) + "\n" + str(parent.half_life("readable"))
    )
    digraph.add_node(parent.nuclide, generation=0, xpos=0, label=node_label)
    seen = {parent.nuclide}

    while len(dequeue) > 0:
        parent_name = dequeue.popleft()
        generation = generations.popleft() + 1
        xpos = xpositions.popleft()
        if generation not in generation_max_xpos:
            generation_max_xpos[generation] = -1
        parent = Nuclide(parent_name, parent.decay_data)

        progeny = parent.progeny()
        branching_fractions = parent.branching_fractions()
        decay_modes = parent.decay_modes()

        if xpos < generation_max_xpos[generation] + 1:
            xpos = generation_max_xpos[generation] + 1
        xcounter = 0
        for idx, prog in enumerate(progeny):
            if prog not in seen:
                node_label = _parse_nuclide_label(prog)
                if prog in parent.decay_data.nuclide_dict:
                    node_label += "\n" + str(
                        parent.decay_data.half_life(prog, "readable")
                    )
                    if np.isfinite(parent.decay_data.half_life(prog)):
                        dequeue.append(prog)
                        generations.append(generation)
                        xpositions.append(xpos + xcounter)
                if prog == "SF":
                    prog = parent.nuclide + "_SF"

                digraph.add_node(
                    prog,
                    generation=generation,
                    xpos=xpos + xcounter,
                    label=node_label,
                )
                seen.add(prog)

                if xpos + xcounter > generation_max_xpos[generation]:
                    generation_max_xpos[generation] = xpos + xcounter
                xcounter += 1

            edge_label = (
                _parse_decay_mode_label(decay_modes[idx])
                + "\n"
                + str(branching_fractions[idx])
            )
            digraph.add_edge(parent.nuclide, prog, label=edge_label)

    for node in digraph:
        digraph.nodes[node]["pos"] = (
            digraph.nodes[node]["xpos"],
            digraph.nodes[node]["generation"] * -1,
        )

    return digraph, max(generation_max_xpos), max(generation_max_xpos.values())
