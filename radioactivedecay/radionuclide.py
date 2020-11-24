"""
The radionuclide module defines the ``Radionuclide`` class. Each ``Radionuclide`` instance contains
decay data for one radionuclide. The data can be accessed via the instance attributes and methods.
The data comes from the ``DecayData`` dataset which is supplied to the ``Radionuclide`` class
constructor (default is radioactivedecay.decaydata.DEFAULTDATA).

The examples shown assume the ``radioactivedecay`` package has been imported as:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

"""

from typing import Dict, List
from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.utils import parse_radionuclide, time_unit_conv


class Radionuclide:
    """
    ``Radionuclide`` instances are used to fetch decay data on one radionuclide. The data comes
    from the assoicated ``DecayData`` dataset.

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
    decay_constant : numpy.float64
        Decay constant of the radionuclide (s\\ :sup:`-1`).
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
        self.decay_constant: float = data.decay_consts[
            data.radionuclide_dict[self.radionuclide]
        ]
        self.prog_bf_mode: Dict[str, List] = data.prog_bfs_modes[
            data.radionuclide_dict[self.radionuclide]
        ]
        self.data: DecayData = data

    def half_life(self, units: str = "s") -> float:
        """
        Returns half-life of the radionuclide in chosen units.

        Parameters
        ----------
        units : str, optional
            Units for half-life (default is seconds). Options are 'ns', 'us', 'ms', 's', 'm', 'h',
            'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', and some of the common spelling variations of
            these time units.

        Returns
        -------
        float
            Radionuclide half-life.

        Examples
        --------
        >>> K40 = rd.Radionuclide('K-40')
        >>> K40.half_life('y')
        1251000000.0

        """

        conv = (
            1.0
            if units == "s"
            else time_unit_conv(
                1.0, units_from="s", units_to=units, year_conv=self.data.year_conv
            )
        )
        return conv * self.data.ln2 / self.decay_constant

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
        decay mode is not a list of all the different radiation types emitted by the decay.

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
