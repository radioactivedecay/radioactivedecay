"""
Unit tests for utils.py functions.
"""

import unittest
import numpy as np
from sympy import Integer, log
from radioactivedecay.utils import (
    Z_to_elem,
    elem_to_Z,
    build_id,
    build_nuclide_string,
    parse_id,
    parse_nuclide_str,
    parse_nuclide,
    add_dictionaries,
    sort_dictionary_alphabetically,
    sort_list_according_to_dataset,
)


class TestFunctions(unittest.TestCase):
    """
    Unit tests for the utils.py functions.
    """

    def test_Z_to_elem(self) -> None:
        """
        Test the conversion of atomic number to element symbol.
        """

        self.assertEqual(Z_to_elem(1), "H")
        self.assertEqual(Z_to_elem(20), "Ca")
        self.assertEqual(Z_to_elem(26), "Fe")

    def test_elem_to_Z(self) -> None:
        """
        Test the conversion of element symbol to atomic number.
        """

        self.assertEqual(elem_to_Z("H"), 1)
        self.assertEqual(elem_to_Z("Ca"), 20)
        self.assertEqual(elem_to_Z("Fe"), 26)

    def test_built_id(self) -> None:
        """
        Test the canonical id builder.
        """

        self.assertEqual(build_id(26, 56), 260560000)
        self.assertEqual(build_id(53, 118), 531180000)
        self.assertEqual(build_id(53, 118, "m"), 531180001)
        self.assertEqual(build_id(65, 156, "n"), 651560002)

        with self.assertRaises(ValueError):
            build_id(65, 156, "z")

    def test_built_nuclide_string(self) -> None:
        """
        Test the nuclide string builder.
        """

        self.assertEqual(build_nuclide_string(26, 56), "Fe-56")
        self.assertEqual(build_nuclide_string(53, 118), "I-118")
        self.assertEqual(build_nuclide_string(53, 118, "m"), "I-118m")
        self.assertEqual(build_nuclide_string(65, 156, "n"), "Tb-156n")

        with self.assertRaises(ValueError):
            build_nuclide_string(999, 1000, "z")

    def test_parse_id(self) -> None:
        """
        Test the canonical id to nuclide string converter.
        """

        self.assertEqual(parse_id(260560000), "Fe-56")
        self.assertEqual(parse_id(531180000), "I-118")
        self.assertEqual(parse_id(531180001), "I-118m")
        self.assertEqual(parse_id(651560002), "Tb-156n")

    def test_parse_nuclide_str(self) -> None:
        """
        Test the parsing of nuclide strings.
        """

        self.assertEqual(parse_nuclide_str("Ca-40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("Ca40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("40Ca"), "Ca-40")

    def test_parse_nuclide(self) -> None:
        """
        Test the parsing of nuclide strings.
        """

        nuclides = np.array(
            [
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
        )
        dataset_name = "test"

        # Re-formatting of acceptable strings e.g. 100Pd -> Pd-100
        self.assertEqual(parse_nuclide("H-3", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("H3", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("3H", nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide(10030000, nuclides, dataset_name), "H-3")
        self.assertEqual(parse_nuclide("Be-7", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("Be7", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("7Be", nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide(40070000, nuclides, dataset_name), "Be-7")
        self.assertEqual(parse_nuclide("C-10", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("C10", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("10C", nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide(60100000, nuclides, dataset_name), "C-10")
        self.assertEqual(parse_nuclide("Ne-19", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("Ne19", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("19Ne", nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide(100190000, nuclides, dataset_name), "Ne-19")
        self.assertEqual(parse_nuclide("I-118", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("I118", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("118I", nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide(531180000, nuclides, dataset_name), "I-118")
        self.assertEqual(parse_nuclide("Pd-100", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("Pd100", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("100Pd", nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide(461000000, nuclides, dataset_name), "Pd-100")
        self.assertEqual(parse_nuclide("Cl-34m", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("Cl34m", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("34mCl", nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide(170340001, nuclides, dataset_name), "Cl-34m")
        self.assertEqual(parse_nuclide("I-118m", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("I118m", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("118mI", nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide(531180001, nuclides, dataset_name), "I-118m")
        self.assertEqual(parse_nuclide("Tb-156m", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("Tb156m", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("156mTb", nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide(651560001, nuclides, dataset_name), "Tb-156m")
        self.assertEqual(parse_nuclide("Tb-156n", nuclides, dataset_name), "Tb-156n")
        self.assertEqual(parse_nuclide("Tb156n", nuclides, dataset_name), "Tb-156n")
        self.assertEqual(parse_nuclide("156nTb", nuclides, dataset_name), "Tb-156n")
        self.assertEqual(parse_nuclide(651560002, nuclides, dataset_name), "Tb-156n")

        # Catch erroneous strings
        with self.assertRaises(TypeError):
            parse_nuclide(1.2, nuclides, dataset_name)
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

    def test_add_dictionaries(self) -> None:
        """
        Test function which adds two inventory dictionaries together.
        """

        dict1 = {"Pm-141": 1.0, "Rb-78": 2.0}
        dict2 = {"Pm-141": 3.0, "Rb-90": 4.0}
        self.assertEqual(
            add_dictionaries(dict1, dict2),
            {"Pm-141": 4.0, "Rb-78": 2.0, "Rb-90": 4.0},
        )

        dict1 = {"Pm-141": Integer(2) * log(3), "Rb-78": Integer(4) / log(5)}
        dict2 = {"Pm-141": log(3) / Integer(7), "Rb-90": Integer(9)}
        self.assertEqual(
            add_dictionaries(dict1, dict2),
            {
                "Pm-141": Integer(15) * log(3) / Integer(7),
                "Rb-78": Integer(4) / log(5),
                "Rb-90": Integer(9),
            },
        )

    def test_sort_dictionary_alphabetically(self) -> None:
        """
        Test the sorting of a dictionary by its keys alphabetically.
        """

        inv_dict = {"U-235": 1.2, "Tc-99m": 2.3, "Tc-99": 5.8}
        self.assertEqual(
            sort_dictionary_alphabetically(inv_dict),
            {"Tc-99": 5.8, "Tc-99m": 2.3, "U-235": 1.2},
        )

        inv_dict = {"U-235": Integer(1), "Tc-99m": Integer(2), "Tc-99": Integer(3)}
        self.assertEqual(
            sort_dictionary_alphabetically(inv_dict),
            {"Tc-99": Integer(3), "Tc-99m": Integer(2), "U-235": Integer(1)},
        )

    def test_sort_list_according_to_dataset(self) -> None:
        """
        Test the sorting of list of nuclides according to their position in the decay dataset.
        """

        nuclide_list = ["Tc-99", "Tc-99m"]
        nuclide_dict = {"Tc-99m": 0, "Tc-99": 1}
        self.assertEqual(
            sort_list_according_to_dataset(nuclide_list, nuclide_dict),
            ["Tc-99m", "Tc-99"],
        )


if __name__ == "__main__":
    unittest.main()
