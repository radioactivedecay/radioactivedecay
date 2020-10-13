"""
Unit tests for decaydata.py functions, classes and methods.
"""

import unittest
from radioactivedecay import decaydata, icrp107


class Test(unittest.TestCase):
    """
    Unit tests for decaydata.py functions, classes and methods.
    """

    def test_decaydata_instantiation(self):
        """
        Test instantiation of DecayData objects.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.dataset, "icrp107")
        self.assertEqual(data.no_radionuclides, 1252)
        self.assertEqual(data.year_conv, 365.2422)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.decay_consts[0], 7.982623693568561e-08)
        self.assertEqual(data.decay_consts[-1], 1.7828715741004621e-09)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)

        # check instantiations with supplied dataset path
        data = decaydata.DecayData("icrp107_2", icrp107.__path__[0])
        self.assertEqual(data.dataset, "icrp107_2")
        self.assertEqual(data.no_radionuclides, 1252)
        self.assertEqual(data.year_conv, 365.2422)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.decay_consts[0], 7.982623693568561e-08)
        self.assertEqual(data.decay_consts[-1], 1.7828715741004621e-09)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)

    def test_decaydata_half_life(self):
        """
        Test DecayData half_life() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.half_life("H-3", "y"), 12.32)

    def test_radionuclide_branching_fraction(self):
        """
        Test DecayData branching_fraction() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.branching_fraction("K-40", "Ca-40"), 0.8914)
        self.assertEqual(data.branching_fraction("K-40", "H-3"), 0.0)

    def test_radionuclide_decay_mode(self):
        """
        Test DecayData decay_mode() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.decay_mode("K-40", "Ca-40"), "\u03b2-")
        self.assertEqual(data.decay_mode("K-40", "H-3"), "")

    def test_decaydata___repr__(self):
        """
        Test DecayData representations.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.__repr__(), "Decay dataset: icrp107")


if __name__ == "__main__":
    unittest.main()
