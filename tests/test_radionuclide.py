"""
Unit tests for radionuclide.py functions, classes and methods.
"""

import unittest
from radioactivedecay import Radionuclide, DecayData


class Test(unittest.TestCase):
    """
    Unit tests for decayfunctions.py functions, classes and methods.
    """

    def test_radionuclide_instantiation(self):
        """
        Test instantiation of Radionuclide objects.
        """

        nuc = Radionuclide("Rn-222")
        self.assertEqual(nuc.radionuclide, "Rn-222")
        self.assertEqual(nuc.prog_bf_mode, {"Po-218": [1.0, "\u03b1"]})

    def test_radionuclide_half_life(self):
        """
        Test Radionuclide half_life() method.
        """

        nuc = Radionuclide("H-3")
        self.assertEqual(nuc.half_life(), 388781329.30560005)
        self.assertEqual(nuc.half_life("y"), 12.32)
        self.assertEqual(nuc.half_life("readable"), "12.32 y")

    def test_radionuclide_progeny(self):
        """
        Test Radionuclide half_life() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.progeny()[0], "Ca-40")
        self.assertEqual(nuc.progeny()[1], "Ar-40")

    def test_radionuclide_branching_fractions(self):
        """
        Test Radionuclide branching_fractions() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.branching_fractions()[0], 0.8914)
        self.assertEqual(nuc.branching_fractions()[1], 0.1086)

    def test_radionuclide_decay_modes(self):
        """
        Test Radionuclide decay_modes() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.decay_modes()[0], "\u03b2-")
        self.assertEqual(nuc.decay_modes()[1], "\u03b2+ & EC")

    def test_radionuclide___repr__(self):
        """
        Test Radionuclide representations.
        """

        nuc = Radionuclide("H-3")
        self.assertEqual(nuc.__repr__(), "Radionuclide: H-3, decay dataset: icrp107")

    def test_radionuclide___eq__(self):
        """
        Test Radionuclide equality.
        """

        nuc1 = Radionuclide("K-40")
        nuc2 = Radionuclide("40K")
        self.assertEqual(nuc1, nuc2)

        data = DecayData("icrp107", load_sympy=True)
        nuc2 = Radionuclide("K-40", data)
        self.assertEqual(nuc1, nuc2)

    def test_radionuclide___ne__(self):
        """
        Test Radionuclide not equality.
        """

        nuc1 = Radionuclide("K-40")
        nuc2 = Radionuclide("H-3")
        self.assertNotEqual(nuc1, nuc2)

    def test_radionuclide___hash__(self):
        """
        Test Radionuclide hash function.
        """

        nuc = Radionuclide("K-40")
        data = DecayData("icrp107", load_sympy=True)
        self.assertEqual(hash(nuc), hash(("K-40", data.dataset)))


if __name__ == "__main__":
    unittest.main()
