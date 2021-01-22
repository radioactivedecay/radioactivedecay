"""
The plots module defines the ``DecayData`` class. Instances of ``DecayData`` initalize by
reading in dataset files containing radioactive decay data. The instances then store the decay
data, and their methods can be used for basic querying of the decay data.

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay.plots as rdplots

"""

from typing import Set, Tuple, Union
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# pylint: disable=too-many-arguments, too-many-locals


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
    plt.show()

    return fig, ax
