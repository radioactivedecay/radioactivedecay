"""
Unit tests for utils.py functions.
"""

import unittest
from sympy import Integer
from radioactivedecay.utils import (
    parse_nuclide_str,
    parse_nuclide,
    time_unit_conv,
    time_unit_conv_sympy,
)


class Test(unittest.TestCase):
    """
    Unit tests for utils.py functions.
    """

    def test_parse_nuclide_str(self):
        """
        Test the parsing of nuclide strings.
        """

        self.assertEqual(parse_nuclide_str("Ca-40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("Ca40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("40Ca"), "Ca-40")

    def test_parse_nuclide(self):
        """
        Test the parsing of radionuclide strings.
        """

        nuclides = [
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
        dataset_name = "test"

        # Re-formatting of acceptable strings e.g. 100Pd -> Pd-100
        self.assertEqual(parse_nuclide("H-3", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("H3", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("3H", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("Be-7", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("Be7", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("7Be", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("C-10", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("C10", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("10C", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("Ne-19", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("Ne19", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("19Ne", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("I-118", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("I118", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("118I", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("Pd-100", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("Pd100", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("100Pd", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("Cl-34m", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("Cl34m", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("34mCl", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("I-118m", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("I118m", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("118mI", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("Tb-156m", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("Tb156m", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("156mTb", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("Tb-156n", nuclides, dataset_name), "Tb-156n")
        self.assertEqual(parse_nuclide("Tb156n", nuclides, dataset_name), "Tb-156n")
        self.assertEqual(parse_nuclide("156nTb", nuclides, dataset_name), "Tb-156n")

        # Catch erroneous strings
        with self.assertRaises(ValueError):
            parse_nuclide("H", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("A1", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("1A", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("H-4", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("H4", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("4H", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("Pb-198m", nuclides, dataset_name)
        with self.assertRaises(ValueError):
            parse_nuclide("Pbo-198m", nuclides, dataset_name)

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
            time_unit_conv(1.0, "s", "y", yconv),
            1.0 / (60.0 ** 2 * 24.0 * 365.2422),
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
