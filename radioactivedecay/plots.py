"""
The plots module defines functions used for creating decay chain diagrams via the Radionuclide
class ``plot()`` method, and activity decay graphs via the Inventory class ``plot()`` method.

"""

from typing import Set, Tuple, Union
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# pylint: disable=too-many-arguments, too-many-locals


def _parse_nuclide_label(nuclide: str) -> str:
    """
    Format a nuclide string to mass number, meta-stable state character in
    superscript, then element symbol. Output is used on node labels in decay
    chain plots.

    Parameters
    ----------
    nuclide : str
        Nuclide string in element-mass format.

    Returns
    -------
    str
        Parsed string for node label in ^{mass}element format.

    """

    if nuclide == "SF":
        return "various"

    nuclide_conversion = {
        "0": "\N{SUPERSCRIPT ZERO}",
        "1": "\N{SUPERSCRIPT ONE}",
        "2": "\N{SUPERSCRIPT TWO}",
        "3": "\N{SUPERSCRIPT THREE}",
        "4": "\N{SUPERSCRIPT FOUR}",
        "5": "\N{SUPERSCRIPT FIVE}",
        "6": "\N{SUPERSCRIPT SIX}",
        "7": "\N{SUPERSCRIPT SEVEN}",
        "8": "\N{SUPERSCRIPT EIGHT}",
        "9": "\N{SUPERSCRIPT NINE}",
        "m": "\N{MODIFIER LETTER SMALL M}",
        "n": "\N{SUPERSCRIPT LATIN SMALL LETTER N}",
        "o": "\N{MODIFIER LETTER SMALL O}",
    }

    element, isotope = nuclide.split("-")
    return "".join(map(lambda char: nuclide_conversion[char], list(isotope))) + element


def _parse_decay_mode_label(mode: str) -> str:
    """
    Format a decay mode string for edge label on decay chain plot.

    Parameters
    ----------
    mode : str
        Decay mode string.

    Returns
    -------
    str
        Formatted decay mode string for use in an edge label.

    """

    mode_conversion = {
        "α": "\N{GREEK SMALL LETTER ALPHA}",
        "β": "\N{GREEK SMALL LETTER BETA}",
        "+": "\N{SUPERSCRIPT PLUS SIGN}",
        "-": "\N{SUPERSCRIPT MINUS}",
    }

    for unformatted, formatted in mode_conversion.items():
        mode = mode.replace(unformatted, formatted)
    return mode


def _decay_graph(
    time_points: np.ndarray,
    activities: np.ndarray,
    radionuclides: np.ndarray,
    xunits: str,
    yunits: Union[None, str],
    xscale: str,
    yscale: str,
    ylimits: np.ndarray,
    display: Set[str],
    fig_in: Union[None, matplotlib.figure.Figure],
    ax_in: Union[None, matplotlib.axes.Axes],
    **kwargs,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """
    Plots a decay graph showing the change in activity of an inventory over time. Creates
    matplotlib fig, ax objects if they are not supplied. Returns fig, ax tuple.

    Parameters
    ----------
    time_points : numpy.ndarray
        Time points for x-axis.
    activities : numpy.ndarray
        Radioactivities for y-axis.
    radionuclides : numpy.ndarray
        NumPy array of the radionuclides (string format is 'H-3', etc.).
    xunits : str
        Units for decay time axis.
    yunits : None or str
        Units for the activity axis
    xscale : str
        The time axis scale type to apply ('linear' or 'log').
    yscale : str
        The activities axis scale type to apply ('linear' or 'log').
    ylimits : numpy.ndarray
        Limits for the y-axis.
    display : set of str
        Radionuclides to display on the graph.
    fig_in : None or matplotlib.figure.Figure
        matplotlib figure object to use, or None creates one.
    ax_in : matplotlib.axes.Axes or None, optional
        matplotlib axes object to use, or None creates one.
    **kwargs
        All additional keyword arguments to supply to matplotlib plot().

    Returns
    -------
    fig : matplotlib.figure.Figure
        matplotlib figure object used to plot decay chain.
    ax : matplotlib.axes.Axes
        matplotlib axes object used to plot decay chain.

    """

    if fig_in is None and ax_in is None:
        fig, ax = plt.subplots()

    for i, label in enumerate(radionuclides):
        if label in display:
            ax.plot(time_points, activities[i], label=label, **kwargs)
    ax.legend(loc="upper right")
    xlabel = "Time (" + xunits + ")"
    ylabel = "Activity (" + yunits + ")" if yunits else "Activity"
    ax.set(
        xlabel=xlabel, ylabel=ylabel, xscale=xscale, yscale=yscale,
    )
    ax.set_ylim(ylimits)

    return fig, ax
