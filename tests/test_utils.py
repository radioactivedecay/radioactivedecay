"""
Unit tests for decayfunctions.py functions, classes and methods.
"""

import unittest
from radioactivedecay.utils import (
    parse_nuclide,
    parse_radionuclide,
    check_dictionary,
    time_unit_conv,
    add_dictionaries,
)


class Test(unittest.TestCase):
    """
    Unit tests for decayfunctions.py functions, classes and methods.
    """

    def test_parse_nuclide(self):
        """
        Test the parsing of nuclide strings.
        """

        self.assertEqual(parse_nuclide("Ca-40"), "Ca-40")
        self.assertEqual(parse_nuclide("Ca40"), "Ca-40")
        self.assertEqual(parse_nuclide("40Ca"), "Ca-40")

    def test_parse_radionuclide(self):
        """
        Test the parsing of radionuclide strings.
        """

        radionuclides = [
            "H-3",
            "Be-7",
            "C-10",
            "Ne-19",
            "I-118",
            "Pd-100",
            "Cl-34m",
            "I-118m",
            "Tb-156m",
            "Tb-156n",
        ]
        dataset = "test"

        # Re-formatting of acceptable strings e.g. 100Pd -> Pd-100
        self.assertEqual(parse_radionuclide("H-3", radionuclides, dataset), "H-3")
        self.assertEqual(parse_radionuclide("H3", radionuclides, dataset), "H-3")
        self.assertEqual(parse_radionuclide("3H", radionuclides, dataset), "H-3")
        self.assertEqual(parse_radionuclide("Be-7", radionuclides, dataset), "Be-7")
        self.assertEqual(parse_radionuclide("Be7", radionuclides, dataset), "Be-7")
        self.assertEqual(parse_radionuclide("7Be", radionuclides, dataset), "Be-7")
        self.assertEqual(parse_radionuclide("C-10", radionuclides, dataset), "C-10")
        self.assertEqual(parse_radionuclide("C10", radionuclides, dataset), "C-10")
        self.assertEqual(parse_radionuclide("10C", radionuclides, dataset), "C-10")
        self.assertEqual(parse_radionuclide("Ne-19", radionuclides, dataset), "Ne-19")
        self.assertEqual(parse_radionuclide("Ne19", radionuclides, dataset), "Ne-19")
        self.assertEqual(parse_radionuclide("19Ne", radionuclides, dataset), "Ne-19")
        self.assertEqual(parse_radionuclide("I-118", radionuclides, dataset), "I-118")
        self.assertEqual(parse_radionuclide("I118", radionuclides, dataset), "I-118")
        self.assertEqual(parse_radionuclide("118I", radionuclides, dataset), "I-118")
        self.assertEqual(parse_radionuclide("Pd-100", radionuclides, dataset), "Pd-100")
        self.assertEqual(parse_radionuclide("Pd100", radionuclides, dataset), "Pd-100")
        self.assertEqual(parse_radionuclide("100Pd", radionuclides, dataset), "Pd-100")
        self.assertEqual(parse_radionuclide("Cl-34m", radionuclides, dataset), "Cl-34m")
        self.assertEqual(parse_radionuclide("Cl34m", radionuclides, dataset), "Cl-34m")
        self.assertEqual(parse_radionuclide("34mCl", radionuclides, dataset), "Cl-34m")
        self.assertEqual(parse_radionuclide("I-118m", radionuclides, dataset), "I-118m")
        self.assertEqual(parse_radionuclide("I118m", radionuclides, dataset), "I-118m")
        self.assertEqual(parse_radionuclide("118mI", radionuclides, dataset), "I-118m")
        self.assertEqual(
            parse_radionuclide("Tb-156m", radionuclides, dataset), "Tb-156m"
        )
        self.assertEqual(
            parse_radionuclide("Tb156m", radionuclides, dataset), "Tb-156m"
        )
        self.assertEqual(
            parse_radionuclide("156mTb", radionuclides, dataset), "Tb-156m"
        )
        self.assertEqual(
            parse_radionuclide("Tb-156n", radionuclides, dataset), "Tb-156n"
        )
        self.assertEqual(
            parse_radionuclide("Tb156n", radionuclides, dataset), "Tb-156n"
        )
        self.assertEqual(
            parse_radionuclide("156nTb", radionuclides, dataset), "Tb-156n"
        )

        # Catch erroneous strings
        with self.assertRaises(ValueError):
            parse_radionuclide("H", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("A1", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("1A", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("H-4", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("H4", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("4H", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("Pb-198m", radionuclides, dataset)
        with self.assertRaises(ValueError):
            parse_radionuclide("Pbo-198m", radionuclides, dataset)

    def test_check_dictionary(self):
        """
        Test the checking of inventory dictionaries.
        """

        radionuclides = ["H-3", "C-14"]
        dataset = "test"

        # Dictionary parsing
        self.assertEqual(
            check_dictionary({"H-3": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            check_dictionary({"H3": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            check_dictionary({"3H": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            check_dictionary({"H-3": 1}, radionuclides, dataset), {"H-3": 1}
        )
        self.assertEqual(
            check_dictionary({"H-3": 1}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            check_dictionary({"H-3": 1.0, "C-14": 2.0}, radionuclides, dataset),
            {"H-3": 1.0, "C-14": 2.0},
        )
        self.assertEqual(
            check_dictionary({"H-3": 1.0, "C-14": 2.0}, radionuclides, dataset),
            {"C-14": 2.0, "H-3": 1.0},
        )

        # Catch incorrect arguments
        with self.assertRaises(ValueError):
            check_dictionary({"H-3": "1.0"}, radionuclides, dataset)
        with self.assertRaises(ValueError):
            check_dictionary({"1.0": "H-3"}, radionuclides, dataset)

    def test_time_unit_conv_seconds(self):
        """
        Test function which converts between seconds and different time units.
        """

        yconv = 365.2422

        self.assertEqual(time_unit_conv(1.0, "s", "s", yconv), 1.0e0)
        self.assertAlmostEqual(
            time_unit_conv(1.0, "s", "ns", yconv), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(time_unit_conv(1.0, "s", "us", yconv), 1.0e6)
        self.assertEqual(time_unit_conv(1.0, "s", "ms", yconv), 1.0e3)
        self.assertEqual(time_unit_conv(1.0, "s", "m", yconv), 1.0 / 60.0)
        self.assertEqual(time_unit_conv(1.0, "s", "h", yconv), 1.0 / (60.0 ** 2))
        self.assertEqual(time_unit_conv(1.0, "s", "d", yconv), 1.0 / (60.0 ** 2 * 24.0))
        self.assertEqual(
            time_unit_conv(1.0, "s", "y", yconv), 1.0 / (60.0 ** 2 * 24.0 * 365.2422),
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "ns", "s", yconv), 1.0e-9, places=(9 + 15)
        )
        self.assertEqual(time_unit_conv(1.0, "us", "s", yconv), 1.0e-6)
        self.assertEqual(time_unit_conv(1.0, "ms", "s", yconv), 1.0e-3)
        self.assertEqual(time_unit_conv(1.0, "m", "s", yconv), 60.0)
        self.assertEqual(time_unit_conv(1.0, "h", "s", yconv), (60.0 ** 2))
        self.assertEqual(time_unit_conv(1.0, "d", "s", yconv), (60.0 ** 2 * 24.0))
        self.assertEqual(
            time_unit_conv(1.0, "y", "s", yconv), (60.0 ** 2 * 24.0 * 365.2422)
        )

        # Catch some incorrect time units
        with self.assertRaises(ValueError):
            time_unit_conv(1.0, "ty", "y", yconv)
        with self.assertRaises(ValueError):
            time_unit_conv(1.0, "y", "ty", yconv)
        with self.assertRaises(ValueError):
            time_unit_conv(1.0, "ty", 1.0, yconv)

    def test_time_unit_conv_spelling_variations(self):
        """
        Test function which converts between spelling variations of different time units.
        """

        yconv = 365.2422

        self.assertEqual(time_unit_conv(1.0, "s", "sec", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "s", "second", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "s", "seconds", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "h", "hr", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "h", "hour", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "h", "hours", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "d", "day", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "d", "days", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "y", "yr", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "y", "year", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "y", "years", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "sec", "s", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "second", "s", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "seconds", "s", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "hr", "h", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "hour", "h", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "hours", "h", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "day", "d", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "days", "d", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "yr", "y", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "year", "y", yconv), 1.0e0)
        self.assertEqual(time_unit_conv(1.0, "years", "y", yconv), 1.0e0)

    def test_time_unit_conv_year_prefixes(self):
        """
        Test function which converts between different year prefixes.
        """

        yconv = 365.2422

        self.assertAlmostEqual(
            time_unit_conv(1.0, "y", "ky", yconv), 1.0e-3, places=(3 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "y", "My", yconv), 1.0e-6, places=(6 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "y", "Gy", yconv), 1.0e-9, places=(9 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "y", "Ty", yconv), 1.0e-12, places=(12 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "y", "Py", yconv), 1.0e-15, places=(15 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "ky", "y", yconv), 1.0e3, places=(15 - 3)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "My", "y", yconv), 1.0e6, places=(15 - 6)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "Gy", "y", yconv), 1.0e9, places=(15 - 9)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "Ty", "y", yconv), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "Py", "y", yconv), 1.0e15, places=(15 - 15)
        )

    def test_add_dictionaries(self):
        """
        Test function which adds two inventory dictionaries together.
        """

        dict1 = {"Pm-141": 1.0, "Rb-78": 2.0}
        dict2 = {"Pm-141": 3.0, "Rb-90": 4.0}
        self.assertEqual(
            add_dictionaries(dict1, dict2), {"Pm-141": 4.0, "Rb-78": 2.0, "Rb-90": 4.0},
        )


if __name__ == "__main__":
    unittest.main()
