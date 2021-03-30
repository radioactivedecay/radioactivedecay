"""
The radionuclide module defines the ``Radionuclide`` class. Each ``Radionuclide`` instance
represents one radionuclide from the associated ``DecayData`` dataset. The methods provide an
access point for the decay data. The default decay dataset used if none is supplied to the
constructor is rd.DEFAULTDATA.

The code examples shown in the docstrings assume the ``radioactivedecay`` package has been imported
as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from collections import deque
from typing import Any, Dict, List, Tuple, Union
import networkx as nx
from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.plots import (
    _parse_nuclide_label,
    _parse_decay_mode_label,
    matplotlib,
    plt,
)
from radioactivedecay.utils import parse_radionuclide

# pylint: disable=too-many-arguments, too-many-locals


class Radionuclide:
    """
    ``Radionuclide`` instances represent one radionuclide from the assoicated ``DecayData``
    dataset.

    Parameters
    ----------
    radionuclide : str
        Radionuclide string.
    data : DecayData, optional
        Decay dataset (default is the ICRP-107 dataset).

    Attributes
    ----------
    radionuclide : str
        Radionuclide string.
    prog_bf_mode : dict
        Dictionary containing direct progeny as keys, and a list containing the branching fraction
        and the decay mode for that progeny as values.
    data : DecayData
        Decay dataset.

    Examples
    --------
    >>> rd.Radionuclide('K-40')
    Radionuclide: K-40, decay dataset: icrp107

    """

    def __init__(self, radionuclide: str, data: DecayData = DEFAULTDATA) -> None:
        self.radionuclide: str = parse_radionuclide(
            radionuclide, data.radionuclides, data.dataset
        )
        self.prog_bf_mode: Dict[str, List] = data.prog_bfs_modes[
            data.radionuclide_dict[self.radionuclide]
        ]
        self.data: DecayData = data

    def half_life(self, units: str = "s") -> Union[float, str]:
        """
        Returns the half-life of the radionuclide as a float in your chosen units, or as
        a human-readable string with appropriate units.

        Parameters
        ----------
        units : str, optional
            Units for half-life. Options are 'ps', 'ns', 'μs', 'us', 'ms', 's', 'm', 'h', 'd', 'y',
            'ky', 'My', 'By', 'Gy', 'Ty', 'Py', and common spelling variations. Default is 's', i.e.
            seconds. Use 'readable' to get a string of the half-life in human-readable units.

        Returns
        -------
        float or str
            Radionuclide half-life.

        Examples
        --------
        >>> K40 = rd.Radionuclide('K-40')
        >>> K40.half_life('y')
        1251000000.0

        """

        return self.data.half_life(self.radionuclide, units)

    def progeny(self) -> List[str]:
        """
        Returns the direct progeny of the radionuclide.

        Returns
        -------
        list
            List of the direct progeny of the radionuclide, ordered by decreasing branching
            fraction.

        Examples
        --------
        >>> K40 = rd.Radionuclide('K-40')
        >>> K40.progeny()
        ['Ca-40', 'Ar-40']

        """

        return list(self.prog_bf_mode.keys())

    def branching_fractions(self) -> List[float]:
        """
        Returns the branching fractions to the direct progeny of the radionuclide.

        Returns
        -------
        list
            List of branching fractions.

        Examples
        --------
        >>> K40 = rd.Radionuclide('K-40')
        >>> K40.branching_fractions()
        [0.8914, 0.1086]

        """

        return [bf_mode[0] for bf_mode in list(self.prog_bf_mode.values())]

    def decay_modes(self) -> List[str]:
        """
        Returns the decay modes for the radionuclide, as defined in the decay dataset. Note: the
        decay mode strings returned are not lists of all the different radiation types emitted
        during the parent to progeny decay processes. They are the labels defined in the decay
        dataset to classify the parent to progeny decay type (e.g. '\u03b1', '\u03b2-' or 'IT').

        Returns
        -------
        list
            List of decay modes.

        Examples
        --------
        >>> K40 = rd.Radionuclide('K-40')
        >>> K40.decay_modes()
        ['\u03b2-', '\u03b2+ & EC']

        """

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
        Plots a diagram of the decay chain of the radionuclide. The creates a NetworkX DiGraph and
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

        """

        digraph, max_generation, max_xpos = _build_decay_digraph(self, nx.DiGraph())

        positions = nx.get_node_attributes(digraph, "pos")
        node_labels = nx.get_node_attributes(digraph, "label")
        edge_labels = nx.get_edge_attributes(digraph, "label")

        if fig is None and ax is None:
            fig, ax = plt.subplots(
                figsize=(3 * max_xpos + 1.5, 3 * max_generation + 1.5)
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

    def __repr__(self) -> str:
        return (
            "Radionuclide: "
            + str(self.radionuclide)
            + ", decay dataset: "
            + self.data.dataset
        )

    def __eq__(self, other) -> bool:
        """
        Check whether two ``Radionuclide`` instances are equal with ``==`` operator.
        """

        return self.radionuclide == other.radionuclide and self.data == other.data

    def __ne__(self, other) -> bool:
        """
        Check whether two ``Radionuclide`` instances are not equal with ``!=`` operator.
        """

        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Hash function for ``Radionuclide`` instances.
        """

        return hash((self.radionuclide, self.data.dataset))


def _build_decay_digraph(
    parent_rn: Radionuclide, digraph=nx.classes.digraph.DiGraph,
) -> nx.classes.digraph.DiGraph:
    """
    Build a networkx DiGraph for the decay chain of this radionuclide.

    Parameters
    ----------
    radionuclide : Radionuclide
        Radionuclide instance of the parent radionuclide of the decay chain.
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

    max_generation = 0
    max_xpos = 0

    parent = parent_rn.radionuclide
    dequeue = deque([parent])
    generations = deque([0])
    xpositions = deque([0])
    node_label = _parse_nuclide_label(parent) + "\n" + parent_rn.half_life("readable")
    digraph.add_node(parent, generation=0, xpos=0, label=node_label)
    seen = {parent}

    while len(dequeue) > 0:
        parent = dequeue.popleft()
        generation = generations.popleft() + 1
        xpos = xpositions.popleft()
        parent_rn = Radionuclide(parent, parent_rn.data)

        progeny = parent_rn.progeny()
        branching_fractions = parent_rn.branching_fractions()
        decay_modes = parent_rn.decay_modes()

        xcounter = 0
        for i, prog in enumerate(progeny):
            if prog not in seen:
                node_label = _parse_nuclide_label(prog)
                if prog in parent_rn.data.radionuclide_dict:
                    node_label += "\n" + parent_rn.data.half_life(prog, "readable")
                    dequeue.append(prog)
                    generations.append(generation)
                    xpositions.append(xpos + i)
                if prog == "SF":
                    prog = parent + "_SF"

                digraph.add_node(
                    prog, generation=generation, xpos=xpos + xcounter, label=node_label,
                )
                seen.add(prog)

                if generation > max_generation:
                    max_generation = generation
                if xpos + xcounter > max_xpos:
                    max_xpos = xpos + xcounter
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

    return digraph, max_generation, max_xpos
