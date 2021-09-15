"""
Unit tests for converts.py classes and methods.
"""

import unittest
import numpy as np
from sympy import Integer, log
from radioactivedecay.converters import (
    AVOGADRO,
    UnitConverterFloat,
    UnitConverterSympy,
    QuantityConverter,
    QuantityConverterSympy,
)


class TestConverters(unittest.TestCase):
    """
    Unit tests for the converters.py constants.
    """

    def test_avogadro(self) -> None:
        """
        Test instantiation of UnitConverterFloat objects.
        """

        self.assertEqual(AVOGADRO, 6.02214076e23)


class TestUnitConverterFloat(unittest.TestCase):
    """
    Unit tests for the converters.py UnitConverterFloat class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of UnitConverterFloat objects.
        """

        year_conv = 365.2422
        uconv = UnitConverterFloat(year_conv)
        self.assertEqual(uconv.time_units["s"], 1.0)
        self.assertEqual(uconv.time_units["y"], 86400.0 * year_conv)
        self.assertEqual(uconv.activity_units["Bq"], 1.0)
        self.assertEqual(uconv.mass_units["g"], 1.0)
        self.assertEqual(uconv.moles_units["mol"], 1.0)

    def test_time_unit_conv_seconds(self) -> None:
        """
        Test conversion between seconds and different time units.
        """

        year_conv = 365.2422
        uconv = UnitConverterFloat(year_conv)

        self.assertEqual(uconv.time_unit_conv(1.0, "s", "s"), 1.0e0)
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "s", "ps"), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "s", "ns"), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "μs"), 1.0e6)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "us"), 1.0e6)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "ms"), 1.0e3)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "m"), 1.0 / 60.0)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "h"), 1.0 / (60.0 ** 2))
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "d"), 1.0 / (60.0 ** 2 * 24.0))
        self.assertEqual(
            uconv.time_unit_conv(1.0, "s", "y"),
            1.0 / (60.0 ** 2 * 24.0 * year_conv),
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "ps", "s"), 1.0e-12, places=(12 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "ns", "s"), 1.0e-9, places=(9 + 15)
        )
        self.assertEqual(uconv.time_unit_conv(1.0, "μs", "s"), 1.0e-6)
        self.assertEqual(uconv.time_unit_conv(1.0, "us", "s"), 1.0e-6)
        self.assertEqual(uconv.time_unit_conv(1.0, "ms", "s"), 1.0e-3)
        self.assertEqual(uconv.time_unit_conv(1.0, "m", "s"), 60.0)
        self.assertEqual(uconv.time_unit_conv(1.0, "h", "s"), (60.0 ** 2))
        self.assertEqual(uconv.time_unit_conv(1.0, "d", "s"), (60.0 ** 2 * 24.0))
        self.assertEqual(
            uconv.time_unit_conv(1.0, "y", "s"), (60.0 ** 2 * 24.0 * year_conv)
        )

        # Catch some incorrect time units
        with self.assertRaises(ValueError):
            uconv.time_unit_conv(1.0, "ty", "y")
        with self.assertRaises(ValueError):
            uconv.time_unit_conv(1.0, "y", "ty")
        with self.assertRaises(ValueError):
            uconv.time_unit_conv(1.0, "ty", 1.0)

    def test_time_unit_conv_spelling_variations(self) -> None:
        """
        Test spelling variations of different time units.
        """

        year_conv = 365.2422
        uconv = UnitConverterFloat(year_conv)

        self.assertEqual(uconv.time_unit_conv(1.0, "s", "sec"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "second"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "s", "seconds"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "h", "hr"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "h", "hour"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "h", "hours"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "d", "day"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "d", "days"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "y", "yr"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "y", "year"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "y", "years"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "sec", "s"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "second", "s"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "seconds", "s"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "hr", "h"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "hour", "h"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "hours", "h"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "day", "d"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "days", "d"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "yr", "y"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "year", "y"), 1.0e0)
        self.assertEqual(uconv.time_unit_conv(1.0, "years", "y"), 1.0e0)

    def test_time_unit_conv_year_prefixes(self) -> None:
        """
        Test conversions between different year prefixes.
        """

        year_conv = 365.2422
        uconv = UnitConverterFloat(year_conv)

        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "ky"), 1.0e-3, places=(3 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "My"), 1.0e-6, places=(6 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "By"), 1.0e-9, places=(9 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "Gy"), 1.0e-9, places=(9 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "Ty"), 1.0e-12, places=(12 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "y", "Py"), 1.0e-15, places=(15 + 15)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "ky", "y"), 1.0e3, places=(15 - 3)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "My", "y"), 1.0e6, places=(15 - 6)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "Gy", "y"), 1.0e9, places=(15 - 9)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "Ty", "y"), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            uconv.time_unit_conv(1.0, "Py", "y"), 1.0e15, places=(15 - 15)
        )

    def test_activity_unit_conv(self) -> None:
        """
        Test conversions between activity units.
        """

        uconv = UnitConverterFloat(365.2422)

        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "Bq"), 1.0e0)
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "pBq"), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "nBq"), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "μBq"), 1.0e6)
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "uBq"), 1.0e6)
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "mBq"), 1.0e3)
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "kBq"), 1.0e-3, places=(3 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "MBq"), 1.0e-6, places=(6 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "GBq"), 1.0e-9, places=(9 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "TBq"), 1.0e-12, places=(12 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "PBq"), 1.0e-15, places=(15 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "EBq"), 1.0e-18, places=(18 + 15)
        )

        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "pCi"),
            1.0e12 / 3.7e10,
            places=(15 - 12),
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "nCi"), 1.0e9 / 3.7e10, places=(15 - 9)
        )
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "μCi"), 1.0e6 / 3.7e10)
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "uCi"), 1.0e6 / 3.7e10)
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "mCi"), 1.0e3 / 3.7e10)
        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "Ci"), 1.0 / 3.7e10)
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "kCi"), 1.0e-3 / 3.7e10, places=(3 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "MCi"), 1.0e-6 / 3.7e10, places=(6 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "GCi"), 1.0e-9 / 3.7e10, places=(9 + 15)
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "TCi"),
            1.0e-12 / 3.7e10,
            places=(12 + 15),
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "PCi"),
            1.0e-15 / 3.7e10,
            places=(15 + 15),
        )
        self.assertAlmostEqual(
            uconv.activity_unit_conv(1.0, "Bq", "ECi"),
            1.0e-18 / 3.7e10,
            places=(18 + 15),
        )

        self.assertEqual(uconv.activity_unit_conv(1.0, "Bq", "dpm"), 1.0 / 60.0)

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            uconv.activity_unit_conv(1.0, "tBq", "Bq")
        with self.assertRaises(ValueError):
            uconv.activity_unit_conv(1.0, "Bq", "tBq")
        with self.assertRaises(ValueError):
            uconv.activity_unit_conv(1.0, "tBq", 1.0)

    def test_mass_unit_conv(self) -> None:
        """
        Test conversions between mass units.
        """

        uconv = UnitConverterFloat(365.2422)

        self.assertEqual(uconv.mass_unit_conv(1.0, "g", "g"), 1.0e0)
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "pg"), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "ng"), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(uconv.mass_unit_conv(1.0, "g", "μg"), 1.0e6)
        self.assertEqual(uconv.mass_unit_conv(1.0, "g", "ug"), 1.0e6)
        self.assertEqual(uconv.mass_unit_conv(1.0, "g", "mg"), 1.0e3)
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "kg"), 1.0e-3, places=(3 + 15)
        )
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "Mg"), 1.0e-6, places=(6 + 15)
        )
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "t"), 1.0e-6, places=(6 + 15)
        )
        self.assertAlmostEqual(
            uconv.mass_unit_conv(1.0, "g", "ton"), 1.0e-6, places=(6 + 15)
        )

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            uconv.mass_unit_conv(1.0, "tg", "g")
        with self.assertRaises(ValueError):
            uconv.mass_unit_conv(1.0, "g", "tg")
        with self.assertRaises(ValueError):
            uconv.mass_unit_conv(1.0, "tg", 1.0)

    def test_moles_unit_conv(self) -> None:
        """
        Test conversions between moles orders of magnitude.
        """

        uconv = UnitConverterFloat(365.2422)

        self.assertEqual(uconv.moles_unit_conv(1.0, "mol", "mol"), 1.0e0)
        self.assertAlmostEqual(
            uconv.moles_unit_conv(1.0, "mol", "pmol"), 1.0e12, places=(15 - 12)
        )
        self.assertAlmostEqual(
            uconv.moles_unit_conv(1.0, "mol", "nmol"), 1.0e9, places=(15 - 9)
        )
        self.assertEqual(uconv.moles_unit_conv(1.0, "mol", "μmol"), 1.0e6)
        self.assertEqual(uconv.moles_unit_conv(1.0, "mol", "umol"), 1.0e6)
        self.assertEqual(uconv.moles_unit_conv(1.0, "mol", "mmol"), 1.0e3)
        self.assertAlmostEqual(
            uconv.moles_unit_conv(1.0, "mol", "kmol"), 1.0e-3, places=(3 + 15)
        )
        self.assertAlmostEqual(
            uconv.moles_unit_conv(1.0, "mol", "Mmol"), 1.0e-6, places=(6 + 15)
        )

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            uconv.moles_unit_conv(1.0, "tmol", "mol")
        with self.assertRaises(ValueError):
            uconv.moles_unit_conv(1.0, "mol", "tmol")
        with self.assertRaises(ValueError):
            uconv.moles_unit_conv(1.0, "tmol", 1.0)

    def test___eq__(self) -> None:
        """
        Test UnitConverterFloat equality.
        """

        uc1 = UnitConverterFloat(365.2422)
        uc2 = UnitConverterFloat(365.2422)
        self.assertEqual(uc1, uc2)

        self.assertFalse(uc1 == "random object")

    def test___neq__(self) -> None:
        """
        Test UnitConverterFloat inequality.
        """

        uc1 = UnitConverterFloat(365.2422)
        uc2 = UnitConverterFloat(365.25)
        self.assertNotEqual(uc1, uc2)

        self.assertTrue(uc1 != "random object")

    def test___repr__(self) -> None:
        """
        Test UnitConverterFloat __repr__ strings.
        """

        uconv = UnitConverterFloat(365.2422)
        self.assertEqual(
            uconv.__repr__(), "UnitConverterFloat using 365.2422 days in a year."
        )


class TestUnitConverterSympy(unittest.TestCase):
    """
    Unit tests for the converters.py UnitConverterSympy class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of UnitConverterSympy objects.
        """

        year_conv = Integer(3652422) / Integer(10000)
        ucs = UnitConverterSympy(year_conv)
        self.assertEqual(ucs.time_units["s"], Integer(1))
        self.assertEqual(ucs.time_units["y"], Integer(86400) * year_conv)
        self.assertEqual(ucs.activity_units["Bq"], Integer(1))
        self.assertEqual(ucs.mass_units["g"], Integer(1))
        self.assertEqual(ucs.moles_units["mol"], Integer(1))

    def test_time_unit_conv(self) -> None:
        """
        Test of the SymPy version of time_unit_conv().
        """

        year_conv = Integer(3652422) / 10000
        ucs = UnitConverterSympy(year_conv)

        self.assertEqual(ucs.time_unit_conv(Integer(1), "ps", "ns"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "ns", "us"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "μs", "ms"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "us", "ms"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "ms", "s"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "s", "m"), 1 / Integer(60))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "m", "h"), 1 / Integer(60))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "h", "d"), 1 / Integer(24))
        self.assertEqual(
            ucs.time_unit_conv(Integer(1), "d", "y"), 10000 / Integer(3652422)
        )
        self.assertEqual(ucs.time_unit_conv(Integer(1), "y", "ky"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "ky", "My"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "My", "By"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "My", "Gy"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "By", "Ty"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Gy", "Ty"), 1 / Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Ty", "Py"), 1 / Integer(1000))

        self.assertEqual(ucs.time_unit_conv(Integer(1), "ns", "ps"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "μs", "ns"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "us", "ns"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "ms", "us"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "s", "ms"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "m", "s"), Integer(60))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "h", "m"), Integer(60))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "d", "h"), Integer(24))
        self.assertEqual(
            ucs.time_unit_conv(Integer(1), "y", "d"), Integer(3652422) / 10000
        )
        self.assertEqual(ucs.time_unit_conv(Integer(1), "ky", "y"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "My", "ky"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "By", "My"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Gy", "My"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Ty", "By"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Ty", "Gy"), Integer(1000))
        self.assertEqual(ucs.time_unit_conv(Integer(1), "Py", "Ty"), Integer(1000))

        # Catch some incorrect time units
        with self.assertRaises(ValueError):
            ucs.time_unit_conv(Integer(1), "ty", "y")
        with self.assertRaises(ValueError):
            ucs.time_unit_conv(Integer(1), "y", "ty")
        with self.assertRaises(ValueError):
            ucs.time_unit_conv(Integer(1), "ty", Integer(1))

    def test_activity_unit_conv(self) -> None:
        """
        Test of the SymPy version of activity_unit_conv().
        """

        year_conv = Integer(3652422) / 10000
        ucs = UnitConverterSympy(year_conv)

        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "pBq", "nBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "nBq", "μBq"), 1 / Integer(1000)
        )
        self.assertEqual(ucs.activity_unit_conv(Integer(1), "μBq", "uBq"), Integer(1))
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "uBq", "mBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "mBq", "Bq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "Bq", "kBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "kBq", "MBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "MBq", "GBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "GBq", "TBq"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "TBq", "PBq"), 1 / Integer(1000)
        )

        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "pBq", "pCi"), 1 / Integer(37000000000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "pCi", "nCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "nCi", "μCi"), 1 / Integer(1000)
        )
        self.assertEqual(ucs.activity_unit_conv(Integer(1), "μCi", "uCi"), Integer(1))
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "uCi", "mCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "mCi", "Ci"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "Ci", "kCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "kCi", "MCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "MCi", "GCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "GCi", "TCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "TCi", "PCi"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "PCi", "ECi"), 1 / Integer(1000)
        )

        self.assertEqual(
            ucs.activity_unit_conv(Integer(1), "Bq", "dpm"), 1 / Integer(60)
        )

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            ucs.activity_unit_conv(Integer(1), "tBq", "Bq")
        with self.assertRaises(ValueError):
            ucs.activity_unit_conv(Integer(1), "Bq", "tBq")
        with self.assertRaises(ValueError):
            ucs.activity_unit_conv(Integer(1), "tBq", Integer(1))

    def test_mass_unit_conv(self) -> None:
        """
        Test of the SymPy version of mass_unit_conv().
        """

        year_conv = Integer(3652422) / 10000
        ucs = UnitConverterSympy(year_conv)

        self.assertEqual(ucs.mass_unit_conv(Integer(1), "pg", "ng"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "ng", "μg"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "μg", "ug"), Integer(1))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "ug", "mg"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "mg", "g"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "g", "kg"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "kg", "Mg"), 1 / Integer(1000))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "Mg", "t"), Integer(1))
        self.assertEqual(ucs.mass_unit_conv(Integer(1), "Mg", "ton"), Integer(1))

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            ucs.mass_unit_conv(Integer(1), "tg", "g")
        with self.assertRaises(ValueError):
            ucs.mass_unit_conv(Integer(1), "g", "tg")
        with self.assertRaises(ValueError):
            ucs.mass_unit_conv(Integer(1), "tg", Integer(1))

    def test_moles_unit_conv(self) -> None:
        """
        Test of the SymPy version of moles_unit_conv().
        """

        year_conv = Integer(3652422) / 10000
        ucs = UnitConverterSympy(year_conv)

        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "pmol", "nmol"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "nmol", "μmol"), 1 / Integer(1000)
        )
        self.assertEqual(ucs.moles_unit_conv(Integer(1), "μmol", "umol"), Integer(1))
        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "umol", "mmol"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "mmol", "mol"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "mol", "kmol"), 1 / Integer(1000)
        )
        self.assertEqual(
            ucs.moles_unit_conv(Integer(1), "kmol", "Mmol"), 1 / Integer(1000)
        )

        # Catch some incorrect activity units
        with self.assertRaises(ValueError):
            ucs.moles_unit_conv(Integer(1), "tmol", "mol")
        with self.assertRaises(ValueError):
            ucs.moles_unit_conv(Integer(1), "mol", "tmol")
        with self.assertRaises(ValueError):
            ucs.moles_unit_conv(Integer(1), "tmol", Integer(1))

    def test___repr__(self) -> None:
        """
        Test UnitConverterSympy __repr__ strings.
        """

        year_conv = Integer(3652422) / 10000
        ucs = UnitConverterSympy(year_conv)
        self.assertEqual(
            ucs.__repr__(), "UnitConverterSympy using 1826211/5000 days in a year."
        )


class TestQuantityConverter(unittest.TestCase):
    """
    Unit tests for the converters.py QuantityConverter class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of QuantityConverter objects.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(qconv.nuclide_dict["He-3"], 1)
        self.assertEqual(qconv.atomic_masses[0], 3.01604928132)
        self.assertEqual(qconv.decay_consts[1], 0)
        self.assertEqual(qconv.avogadro, 6.02214076e23)

    def test_activity_to_number(self) -> None:
        """
        Test the conversion of activity in Bq to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(qconv.activity_to_number("H-3", 1.0), 560892895.7794082)

    def test_mass_to_number(self) -> None:
        """
        Test the conversion of mass in grams to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(qconv.mass_to_number("H-3", 1.0), 1.996698395247825e23)
        self.assertEqual(qconv.mass_to_number("He-3", 1.0), 1.9967116089131645e23)

    def test_moles_to_number(self) -> None:
        """
        Test the conversion of number of moles to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(qconv.moles_to_number(1.0), 6.02214076e23)
        self.assertEqual(qconv.moles_to_number(0.0), 0.0)

    def test_number_to_activity(self) -> None:
        """
        Test the conversion of number of atoms to activity in Bq.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(qconv.number_to_activity("H-3", 560892895.7794082), 1.0)
        self.assertEqual(qconv.number_to_activity("He-3", 1.0), 0.0)
        self.assertEqual(qconv.number_to_activity("He-3", 0.0), 0.0)

    def test_number_to_mass(self) -> None:
        """
        Test the conversion of number of atoms to mass in grams.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(qconv.number_to_mass("H-3", 1.996698395247825e23), 1.0)
        self.assertEqual(qconv.number_to_mass("He-3", 1.9967116089131645e23), 1.0)

    def test_number_to_moles(self) -> None:
        """
        Test the conversion of number of atoms to number of moles.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(qconv.number_to_moles(6.02214076e23), 1.0)
        self.assertEqual(qconv.number_to_moles(0.0), 0.0)

    def test___eq__(self) -> None:
        """
        Test QuantityConveter equality.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv1 = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        qconv2 = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(qconv1, qconv2)

        self.assertFalse(qconv1 == "random object")

    def test___neq__(self) -> None:
        """
        Test QuantityConveter inequality.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv1 = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        decay_consts = np.array([1.7828715741004621e-09, 0.1])
        qconv2 = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        self.assertNotEqual(qconv1, qconv2)

        self.assertTrue(qconv1 != "random object")

    def test___repr__(self) -> None:
        """
        Test QuantityConveter __repr__ strings.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = np.array([3.01604928132, 3.01602932197])
        decay_consts = np.array([1.7828715741004621e-09, 0.0])
        qconv = QuantityConverter(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(
            qconv.__repr__(), "QuantityConverter using double-precision floats."
        )


class TestQuantityConverterSympy(unittest.TestCase):
    """
    Unit tests for the converters.py QuantityConverterSympy class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of QuantityConverter objects.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]

        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(qcs.nuclide_dict["He-3"], 1)
        self.assertEqual(
            qcs.atomic_masses[0],
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
        )
        self.assertEqual(qcs.decay_consts[1], Integer(0))
        self.assertEqual(qcs.avogadro, Integer(602214076000000000000000))

    def test_activity_to_number(self) -> None:
        """
        Test the conversion of activity in Bq to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.activity_to_number("H-3", Integer(1)),
            Integer(242988330816) / (Integer(625) * log(2)),
        )

    def test_mass_to_number(self) -> None:
        """
        Test the conversion of mass in grams to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.mass_to_number("H-3", Integer(1)),
            Integer(75401232033)
            / Integer("15055351900000000000000000000000000")
            * Integer("602214076000000000000000"),
        )
        self.assertEqual(
            qcs.mass_to_number("He-3", Integer(1)),
            Integer(301602932197)
            / Integer("60221407600000000000000000000000000")
            * Integer("602214076000000000000000"),
        )

    def test_moles_to_number(self) -> None:
        """
        Test the conversion of number of moles to number of atoms.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.moles_to_number(Integer(1)), Integer("602214076000000000000000")
        )
        self.assertEqual(qcs.moles_to_number(Integer(0)), Integer(0))

    def test_number_to_activity(self) -> None:
        """
        Test the conversion of number of atoms to activity in Bq.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.number_to_activity("H-3", Integer(1)),
            Integer(625) * log(2) / Integer(242988330816),
        )
        self.assertEqual(qcs.number_to_activity("He-3", Integer(0)), Integer(0))
        self.assertEqual(qcs.number_to_activity("He-3", Integer(0)), Integer(0))

    def test_number_to_mass(self) -> None:
        """
        Test the conversion of number of atoms to mass in grams.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.number_to_mass("H-3", Integer(1)),
            Integer("15055351900000000000000000000000000")
            / Integer(75401232033)
            / Integer("602214076000000000000000"),
        )
        self.assertEqual(
            qcs.number_to_mass("He-3", Integer(1)),
            Integer("60221407600000000000000000000000000")
            / Integer(301602932197)
            / Integer("602214076000000000000000"),
        )

    def test_number_to_moles(self) -> None:
        """
        Test the conversion of number of atoms to number of moles.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.number_to_moles(Integer("602214076000000000000000")), Integer(1)
        )
        self.assertEqual(qcs.number_to_moles(Integer(0)), Integer(0))

    def test___eq__(self) -> None:
        """
        Test QuantityConveterSympy equality.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qconv1 = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)
        qconv2 = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)
        self.assertEqual(qconv1, qconv2)

        self.assertFalse(qconv1 == "random object")

    def test___repr__(self) -> None:
        """
        Test QuantityConveterSympy __repr__ strings.
        """

        nuclide_dict = {"H-3": 0, "He-3": 1}
        atomic_masses = [
            Integer("15055351900000000000000000000000000") / Integer(75401232033),
            Integer("60221407600000000000000000000000000") / Integer(301602932197),
        ]
        decay_consts = [(Integer(625) * log(2)) / Integer(242988330816), Integer(0)]
        qcs = QuantityConverterSympy(nuclide_dict, atomic_masses, decay_consts)

        self.assertEqual(
            qcs.__repr__(),
            "QuantityConverterSympy using SymPy arbitrary precision calculations.",
        )


if __name__ == "__main__":
    unittest.main()
