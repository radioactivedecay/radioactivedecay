"""
Unit tests for decayfunctions.py functions, classes and methods.
"""

import unittest
from sympy import Integer
from radioactivedecay.utils import (
    parse_nuclide,
    parse_radionuclide,
    time_unit_conv,
    time_unit_conv_sympy,
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

    def test_time_unit_conv_seconds(self):
        """
        Test function which converts between seconds and different time units.
        """

        yconv = 365.2422

        self.assertEqual(time_unit_conv(1.0, "s", "s", yconv), 1.0e0)
        self.assertAlmostEqual(
            time_unit_conv(1.0, "s", "ps", yconv), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "s", "ns", yconv), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(time_unit_conv(1.0, "s", "μs", yconv), 1.0e6)
        self.assertEqual(time_unit_conv(1.0, "s", "us", yconv), 1.0e6)
        self.assertEqual(time_unit_conv(1.0, "s", "ms", yconv), 1.0e3)
        self.assertEqual(time_unit_conv(1.0, "s", "m", yconv), 1.0 / 60.0)
        self.assertEqual(time_unit_conv(1.0, "s", "h", yconv), 1.0 / (60.0 ** 2))
        self.assertEqual(time_unit_conv(1.0, "s", "d", yconv), 1.0 / (60.0 ** 2 * 24.0))
        self.assertEqual(
            time_unit_conv(1.0, "s", "y", yconv), 1.0 / (60.0 ** 2 * 24.0 * 365.2422),
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "ps", "s", yconv), 1.0e-12, places=(12 + 15)
        )
        self.assertAlmostEqual(
            time_unit_conv(1.0, "ns", "s", yconv), 1.0e-9, places=(9 + 15)
        )
        self.assertEqual(time_unit_conv(1.0, "μs", "s", yconv), 1.0e-6)
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
            time_unit_conv(1.0, "y", "By", yconv), 1.0e-9, places=(9 + 15)
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

    def test_time_unit_conv_sympy(self):
        """
        Test of the variation of time_unit_conv() which uses SymPy objects.
        """

        yconv = Integer(3652422) / 10000

        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ps", "ns", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ns", "us", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "μs", "ms", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "us", "ms", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ms", "s", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "s", "m", yconv), 1 / Integer(60)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "m", "h", yconv), 1 / Integer(60)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "h", "d", yconv), 1 / Integer(24)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "d", "y", yconv), 10000 / Integer(3652422)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "y", "ky", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ky", "My", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "My", "By", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "My", "Gy", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "By", "Ty", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Gy", "Ty", yconv), 1 / Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Ty", "Py", yconv), 1 / Integer(1000)
        )

        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ns", "ps", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "μs", "ns", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "us", "ns", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ms", "us", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "s", "ms", yconv), Integer(1000)
        )
        self.assertEqual(time_unit_conv_sympy(Integer(1), "m", "s", yconv), Integer(60))
        self.assertEqual(time_unit_conv_sympy(Integer(1), "h", "m", yconv), Integer(60))
        self.assertEqual(time_unit_conv_sympy(Integer(1), "d", "h", yconv), Integer(24))
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "y", "d", yconv), Integer(3652422) / 10000
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "ky", "y", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "My", "ky", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "By", "My", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Gy", "My", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Ty", "By", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Ty", "Gy", yconv), Integer(1000)
        )
        self.assertEqual(
            time_unit_conv_sympy(Integer(1), "Py", "Ty", yconv), Integer(1000)
        )

        # Catch some incorrect time units
        with self.assertRaises(ValueError):
            time_unit_conv_sympy(1.0, "ty", "y", yconv)
        with self.assertRaises(ValueError):
            time_unit_conv_sympy(1.0, "y", "ty", yconv)
        with self.assertRaises(ValueError):
            time_unit_conv_sympy(1.0, "ty", 1.0, yconv)


if __name__ == "__main__":
    unittest.main()
