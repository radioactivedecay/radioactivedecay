"""
Unit tests for utils.py functions.
"""

import unittest
from sympy import Integer, log
from radioactivedecay.utils import (
    parse_nuclide_str,
    parse_nuclide,
    add_dictionaries,
    sort_dictionary_alphabetically,
    sort_list_according_to_dataset,
)


class TestUtilsFunctions(unittest.TestCase):
    """
    Unit tests for the utils.py functions.
    """

    def test_parse_nuclide_str(self) -> None:
        """
        Test the parsing of nuclide strings.
        """

        self.assertEqual(parse_nuclide_str("Ca-40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("Ca40"), "Ca-40")
        self.assertEqual(parse_nuclide_str("40Ca"), "Ca-40")

    def test_parse_nuclide(self) -> None:
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
