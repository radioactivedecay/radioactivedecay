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

from typing import Dict, List, Union
from radioactivedecay.decaydata import DecayData, DEFAULTDATA
from radioactivedecay.utils import parse_radionuclide


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
