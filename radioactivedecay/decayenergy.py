"""
The decayenergy module loads in the decay energies data sets, and defines two key functions for
calculating decay energy

All data comes from this website: https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html#dcy2

The docstring code examples assume that ``radioactivedecay`` has been imported
as ``rd``:

.. highlight:: python
.. code-block:: python

    >>> import radioactivedecay as rd

Constants
---------
EV_TO_WH : conversion from electron volts to watt hours
DECAY_ENERGIES: Map of isotopes to the energy the release per decay type
META_ENERGIES: Map of isotopes metastable version to the energy they release 
    when returning to the normal state
MODE_MAP: map that converts the decay modes found in this package 
    to the types used by the source data
"""

from importlib import resources
import math
import pickle
from typing import Dict, List, Tuple


EV_TO_WH = 1.602176634 * 10e-19

MODE_MAP = {"α": "A", "β-": "B-", "β+": "B+", "EC": "EC", "SF": "SF", "IT": "IT"}


def transform_decay_modes(modes: List[str]) -> List[str]:
    return [MODE_MAP[m] for m in modes]


def _load_data() -> Tuple[Dict[str, dict], Dict[str, dict]]:
    """
    Loads the decay energy data and the decay metastable energy for energy calculations.
    """
    isotope_map = {}
    metastable_map = {}

    with resources.files(f"{__package__}.decay_energies").joinpath(
        "decay_energies.pickle"
    ).open("rb") as file:
        decay_energies = pickle.load(file)

        for _, row in decay_energies.iterrows():
            isotope_name = f"{row['symbol']}-{row['z'] + row['n']}"
            row_dict = {}
            row_dict["A"] = row["qa"]
            row_dict["B-"] = row["qbm"]
            row_dict["B-N"] = row["qbm_n"]
            row_dict["EC"] = row["qec"]

            for k, v in row_dict.items():
                if math.isnan(v):
                    row_dict[k] = 0

            isotope_map[isotope_name] = row_dict

    with resources.files(f"{__package__}.decay_energies").joinpath(
        "meta_energies.pickle"
    ).open("rb") as file:
        meta_energies = pickle.load(file)
        for _, row in meta_energies.iterrows():
            isotope_name = f"{row['symbol']}-{row['z'] + row['n']}"
            metastable_map[isotope_name] = row["energy"]

    return isotope_map, metastable_map


DECAY_ENERGIES, META_ENERGIES = _load_data()


def get_decay_energy_for_isotope(isotope: str, units="ev") -> Dict[str, float]:
    """
    Returns a dictionary containing the energy released per type of radiation

    Parameters
    ----------
    isotope: isotope name in 'H-3' format
    units : str, optional
        energy units for output, ev or wh
        Deafult is 'ev'.

    Examples
    --------
    >>> get_decay_energy_for_isotope('H-3')
    {"B-": 18.59202}
    """
    convert_to_watt_hours = units == "wh"

    is_metastable = isotope[-1] == "m"
    isotope = isotope.rstrip("m")
    energies = DECAY_ENERGIES[isotope]
    if is_metastable:
        meta_energy = META_ENERGIES[isotope]
        energies["IT"] = meta_energy

    if convert_to_watt_hours:
        for k, v in energies:
            energies[k] = v * EV_TO_WH

    return energies
