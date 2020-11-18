"""
Unit tests for radionuclide.py functions, classes and methods.
"""

import unittest
import radioactivedecay as rd


class Test(unittest.TestCase):
    """
    Unit tests for decayfunctions.py functions, classes and methods.
    """

    def test_radionuclide_instantiation(self):
        """
        Test instantiation of Radionuclide objects.
        """

        nuc = rd.Radionuclide("Rn-222")
        self.assertEqual(nuc.radionuclide, "Rn-222")
        self.assertEqual(nuc.decay_constant, 2.0982180755947176e-06)
        self.assertEqual(nuc.prog_bf_mode, {"Po-218": [1.0, "\u03b1"]})

    def test_radionuclide_half_life(self):
        """
        Test Radionuclide half_life() method.
        """

        nuc = rd.Radionuclide("H-3")
        self.assertEqual(nuc.half_life("y"), 12.32)

    def test_radionuclide_progeny(self):
        """
        Test Radionuclide half_life() method.
        """

        nuc = rd.Radionuclide("K-40")
        self.assertEqual(nuc.progeny()[0], "Ca-40")
        self.assertEqual(nuc.progeny()[1], "Ar-40")

    def test_radionuclide_branching_fractions(self):
        """
        Test Radionuclide branching_fractions() method.
        """

        nuc = rd.Radionuclide("K-40")
        self.assertEqual(nuc.branching_fractions()[0], 0.8914)
        self.assertEqual(nuc.branching_fractions()[1], 0.1086)

    def test_radionuclide_decay_modes(self):
        """
        Test Radionuclide decay_modes() method.
        """

        nuc = rd.Radionuclide("K-40")
        self.assertEqual(nuc.decay_modes()[0], "\u03b2-")
        self.assertEqual(nuc.decay_modes()[1], "\u03b2+ & EC")

    def test_radionuclide___repr__(self):
        """
        Test Radionuclide representations.
        """

        nuc = rd.Radionuclide("H-3")
        self.assertEqual(nuc.__repr__(), "Radionuclide: H-3, Decay dataset: icrp107")


if __name__ == "__main__":
    unittest.main()
