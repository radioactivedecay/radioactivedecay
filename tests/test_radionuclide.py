"""
Unit tests for radionuclide.py functions, classes and methods.
"""

import unittest
from radioactivedecay.decaydata import DecayData
from radioactivedecay.radionuclide import Radionuclide


class TestRadionuclide(unittest.TestCase):
    """
    Unit tests for the radionuclide.py Radionuclide class.
    """

    def test_radionuclide_instantiation(self) -> None:
        """
        Test instantiation of Radionuclide objects.
        """

        nuc = Radionuclide("Rn-222")
        self.assertEqual(nuc.nuclide, "Rn-222")
        self.assertEqual(nuc.prog_bf_mode, {"Po-218": [1.0, "\u03b1"]})

    def test_radionuclide_half_life(self) -> None:
        """
        Test Radionuclide half_life() method.
        """

        nuc = Radionuclide("H-3")
        self.assertEqual(nuc.half_life(), 388781329.30560005)
        self.assertEqual(nuc.half_life("y"), 12.32)
        self.assertEqual(nuc.half_life("readable"), "12.32 y")

    def test_radionuclide_progeny(self) -> None:
        """
        Test Radionuclide half_life() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.progeny()[0], "Ca-40")
        self.assertEqual(nuc.progeny()[1], "Ar-40")

    def test_radionuclide_branching_fractions(self) -> None:
        """
        Test Radionuclide branching_fractions() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.branching_fractions()[0], 0.8914)
        self.assertEqual(nuc.branching_fractions()[1], 0.1086)

    def test_radionuclide_decay_modes(self) -> None:
        """
        Test Radionuclide decay_modes() method.
        """

        nuc = Radionuclide("K-40")
        self.assertEqual(nuc.decay_modes()[0], "\u03b2-")
        self.assertEqual(nuc.decay_modes()[1], "\u03b2+ & EC")

    def test_radionuclide_plot(self) -> None:
        """
        Test Radionuclide plot() method.

        Only testing auto-generation of limits so far.
        """

        nuc = Radionuclide("H-3")
        _, axes = nuc.plot()
        self.assertEqual(axes.get_xlim(), (-0.3, 0.3))
        self.assertEqual(axes.get_ylim(), (-1.3, 0.3))

        nuc = Radionuclide("Mo-99")
        _, axes = nuc.plot()
        self.assertEqual(axes.get_xlim(), (-0.3, 1.3))
        self.assertEqual(axes.get_ylim(), (-2.3, 0.3))

        nuc = Radionuclide("Es-256")
        _, axes = nuc.plot()
        self.assertEqual(axes.get_xlim(), (-0.3, 2.3))
        self.assertEqual(axes.get_ylim(), (-19.3, 0.3))

    def test_radionuclide___repr__(self) -> None:
        """
        Test Radionuclide __repr__ strings.
        """

        nuc = Radionuclide("H-3")
        self.assertEqual(
            nuc.__repr__(),
            "Radionuclide: H-3, decay dataset: icrp107_ame2020_nubase2020",
        )

    def test_radionuclide___eq__(self) -> None:
        """
        Test Radionuclide equality.
        """

        nuc1 = Radionuclide("K-40")
        nuc2 = Radionuclide("40K")
        self.assertEqual(nuc1, nuc2)

        decay_data = DecayData("icrp107_ame2020_nubase2020", load_sympy=True)
        nuc2 = Radionuclide("K-40", decay_data)
        self.assertEqual(nuc1, nuc2)

        self.assertFalse(nuc1 == "random object")

    def test_radionuclide___ne__(self) -> None:
        """
        Test Radionuclide inequality.
        """

        nuc1 = Radionuclide("K-40")
        nuc2 = Radionuclide("H-3")
        self.assertNotEqual(nuc1, nuc2)

        self.assertTrue(nuc1 != "random object")

    def test_radionuclide___hash__(self) -> None:
        """
        Test Radionuclide hash function.
        """

        nuc = Radionuclide("K-40")
        decay_data = DecayData("icrp107_ame2020_nubase2020", load_sympy=True)
        self.assertEqual(hash(nuc), hash(("K-40", decay_data.dataset_name)))


if __name__ == "__main__":
    unittest.main()
