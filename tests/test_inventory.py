"""
Unit tests for inventory.py functions, classes and methods.
"""

import copy
import unittest
from unittest.mock import patch
from radioactivedecay.inventory import (
    _add_dictionaries,
    _sort_dictionary_alphabetically,
    _check_dictionary,
    _sort_list_according_to_dataset,
    Inventory,
)
from radioactivedecay import DEFAULTDATA, DecayData, Radionuclide


class Test(unittest.TestCase):
    """
    Unit tests for decayfunctions.py functions, classes and methods.
    """

    # pylint: disable=too-many-public-methods

    def test__add_dictionaries(self):
        """
        Test function which adds two inventory dictionaries together.
        """

        dict1 = {"Pm-141": 1.0, "Rb-78": 2.0}
        dict2 = {"Pm-141": 3.0, "Rb-90": 4.0}
        self.assertEqual(
            _add_dictionaries(dict1, dict2),
            {"Pm-141": 4.0, "Rb-78": 2.0, "Rb-90": 4.0},
        )

    def test__sort_dictionary_alphabetically(self):
        """
        Test the sorting of a dictionary by its keys alphabetically.
        """

        inv_dict = {"U-235": 1.2, "Tc-99m": 2.3, "Tc-99": 5.8}
        self.assertEqual(
            _sort_dictionary_alphabetically(inv_dict),
            {"Tc-99": 5.8, "Tc-99m": 2.3, "U-235": 1.2},
        )

    def test__check_dictionary(self):
        """
        Test the checking of inventory dictionaries.
        """

        radionuclides = ["H-3", "C-14"]
        H3 = Radionuclide("H3")
        C14 = Radionuclide("C14")
        dataset = "test"

        # Dictionary parsing
        self.assertEqual(
            _check_dictionary({"H-3": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            _check_dictionary({"H3": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            _check_dictionary({"3H": 1.0}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            _check_dictionary({"H-3": 1}, radionuclides, dataset), {"H-3": 1}
        )
        self.assertEqual(
            _check_dictionary({"H-3": 1}, radionuclides, dataset), {"H-3": 1.0}
        )
        self.assertEqual(
            _check_dictionary({"H-3": 1.0, "C-14": 2.0}, radionuclides, dataset),
            {"H-3": 1.0, "C-14": 2.0},
        )
        self.assertEqual(
            _check_dictionary({"H-3": 1.0, "C-14": 2.0}, radionuclides, dataset),
            {"C-14": 2.0, "H-3": 1.0},
        )
        self.assertEqual(
            _check_dictionary({H3: 1.0, C14: 2.0}, radionuclides, dataset),
            {"C-14": 2.0, "H-3": 1.0},
        )
        self.assertEqual(
            _check_dictionary({"H-3": 1.0, C14: 2.0}, radionuclides, dataset),
            {"C-14": 2.0, "H-3": 1.0},
        )
        self.assertEqual(
            _check_dictionary({H3: 1.0, "C-14": 2.0}, radionuclides, dataset),
            {"C-14": 2.0, "H-3": 1.0},
        )

        # Catch incorrect arguments
        with self.assertRaises(ValueError):
            _check_dictionary({"H-3": "1.0"}, radionuclides, dataset)
        with self.assertRaises(ValueError):
            _check_dictionary({"1.0": "H-3"}, radionuclides, dataset)

    def test__sort_list_according_to_dataset(self):
        """
        Test the sorting of list of radionuclides according to their position in the decay dataset.
        """

        radionuclide_list = ["Tc-99", "Tc-99m"]
        self.assertEqual(
            _sort_list_according_to_dataset(
                radionuclide_list, DEFAULTDATA.radionuclide_dict
            ),
            ["Tc-99m", "Tc-99"],
        )

    def test_inventory_instantiation(self):
        """
        Test instantiation of Inventory objects.
        """

        inv = Inventory({"H-3": 1.0})
        self.assertEqual(inv.contents, {"H-3": 1.0})

        inv = Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

        Tc99m = Radionuclide("Tc-99m")
        inv = Inventory({Tc99m: 2.3, "I-123": 5.8})
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

        I123 = Radionuclide("I-123")
        inv = Inventory({"Tc-99m": 2.3, I123: 5.8})
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

    def test_inventory__change(self):
        """
        Test Inventory _change() method.
        """

        inv = Inventory({"H-3": 1.0})
        inv._change({"Tc-99m": 2.3, "I-123": 5.8}, True, DEFAULTDATA)
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

        Tc99m = Radionuclide("Tc-99m")
        inv = Inventory({"H-3": 1.0})
        inv._change({Tc99m: 2.3, "I-123": 5.8}, True, DEFAULTDATA)
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

    def test_inventory_radionuclides(self):
        """
        Test Inventory radionuclides property.
        """

        inv = Inventory({"H-3": 1.0})
        self.assertEqual(inv.radionuclides, ["H-3"])
        inv = Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.radionuclides, ["I-123", "Tc-99m"])

    def test_inventory_activities(self):
        """
        Test Inventory activities property.
        """

        inv = Inventory({"H-3": 1})
        self.assertEqual(inv.activities, [1.0])
        inv = Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.activities, [5.8, 2.3])

    def test_inventory___len__(self):
        """
        Test len() on Inventory.
        """

        inv = Inventory({"H-3": 1})
        self.assertEqual(len(inv), 1)
        inv = Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(len(inv), 2)

    def test_inventory_add(self):
        """
        Test Inventory add() method to append to an inventory.
        """

        inv = Inventory({"H-3": 1})
        inv.add({"C-14": 3.0, "K-40": 4.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 1.0, "K-40": 4.0})
        inv.add({"H-3": 3.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})

        inv = Inventory({"H-3": 1})
        inv.add({Radionuclide("C-14"): 3.0, "K-40": 4.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 1.0, "K-40": 4.0})
        inv.add({Radionuclide("H-3"): 3.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})

    def test_inventory_subtract(self):
        """
        Test Inventory subtract() method to take away a dictionary from an inventory.
        """

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.subtract({"C-14": 3.0, "K-40": 4.0})
        self.assertEqual(inv.contents, {"C-14": 0.0, "H-3": 4.0, "K-40": 0.0})

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.subtract({"C-14": 3.0, Radionuclide("K-40"): 4.0})
        self.assertEqual(inv.contents, {"C-14": 0.0, "H-3": 4.0, "K-40": 0.0})

    def test_inventory___add__(self):
        """
        Test operator to add two inventory objects together.
        """

        inv1 = Inventory({"H-3": 1.0})
        inv2 = Inventory({"C-14": 1.0, "H-3": 4.0})
        inv = inv1 + inv2
        self.assertEqual(inv.contents, {"C-14": 1.0, "H-3": 5.0})

        temp_data = copy.deepcopy(DEFAULTDATA)
        temp_data.dataset = "icrp107_"
        inv3 = Inventory({"H-3": 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 + inv3

    def test_inventory___subtract__(self):
        """
        Test operator to subtract one inventory object from another.
        """

        inv1 = Inventory({"H-3": 1.0})
        inv2 = Inventory({"C-14": 1.0, "H-3": 4.0})
        inv = inv2 - inv1
        self.assertEqual(inv.contents, {"C-14": 1.0, "H-3": 3.0})

        temp_data = copy.deepcopy(DEFAULTDATA)
        temp_data.dataset = "icrp107_"
        inv3 = Inventory({"H-3": 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 - inv3

    def test_inventory___mul__(self):
        """
        Test operator to multiply activities in inventory by constant.
        """

        inv = Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = inv * 2
        self.assertEqual(inv.contents, {"Cs-137": 2.0, "Sr-90": 2.0})

    def test_inventory___rmul__(self):
        """
        Test operator to right multiply constant by activities in inventory.
        """

        inv = Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = 2 * inv
        self.assertEqual(inv.contents, {"Cs-137": 2.0, "Sr-90": 2.0})

    def test_inventory___truediv__(self):
        """
        Test operator to multiply activities in inventory by constant.
        """

        inv = Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = inv / 2
        self.assertEqual(inv.contents, {"Cs-137": 0.5, "Sr-90": 0.5})

    def test_inventory_remove(self):
        """
        Test operator to remove radionuclides from an inventory.
        """

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        with self.assertRaises(NotImplementedError):
            inv.remove(1.0)

    def test_inventory_remove_string(self):
        """
        Test operator to remove one radionuclide from an inventory using a radionuclide string.
        """

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove("H-3")
        self.assertEqual(inv.contents, {"C-14": 3.0, "K-40": 4.0})

        with self.assertRaises(ValueError):
            inv.remove("Be-10")

    def test_inventory_remove_radionuclide(self):
        """
        Test operator to remove one radionuclide from an inventory using a ``Radionuclide`` object.
        """

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove(Radionuclide("H-3"))
        self.assertEqual(inv.contents, {"C-14": 3.0, "K-40": 4.0})

        with self.assertRaises(ValueError):
            inv.remove(Radionuclide("Be-10"))

    def test_inventory_remove_list(self):
        """
        Test operator to remove list of radionuclides from an inventory.
        """

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove(["H-3", "C-14"])
        self.assertEqual(inv.contents, {"K-40": 4.0})

        with self.assertRaises(ValueError):
            inv.remove(["Be-10", "C-14"])

        inv = Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove(["H-3", Radionuclide("C-14")])
        self.assertEqual(inv.contents, {"K-40": 4.0})

    def test_inventory_decay(self):
        """
        Test Inventory decay() calculations.
        """

        inv = Inventory({"H-3": 10.0})
        self.assertEqual(inv.decay(12.32, "y").contents, {"H-3": 5.0})
        inv = Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(
            inv.decay(20.0, "h").contents,
            {
                "I-123": 2.040459244534774,
                "Tc-99": 6.729944738772211e-09,
                "Tc-99m": 0.22950748010063513,
                "Te-123": 9.485166535243877e-18,
                "Te-123m": 7.721174031572363e-07,
            },
        )
        inv = Inventory({"U-238": 99.274, "U-235": 0.720, "U-234": 0.005})
        self.assertEqual(
            inv.decay(1e9, "y").contents,
            {
                "Ac-227": 0.2690006281740556,
                "At-218": 0.017002868638497183,
                "At-219": 2.227325201281319e-07,
                "Bi-210": 85.01434361515662,
                "Bi-211": 0.26900084425585846,
                "Bi-214": 85.01432618961896,
                "Bi-215": 2.1605054452429237e-07,
                "Fr-223": 0.0037122086688021884,
                "Hg-206": 1.6152725286830197e-06,
                "Pa-231": 0.2690006198549055,
                "Pa-234": 0.13601313171698984,
                "Pa-234m": 85.00820732310412,
                "Pb-210": 85.01434361489548,
                "Pb-211": 0.2690008442558569,
                "Pb-214": 84.99734032384839,
                "Po-210": 85.01434362236536,
                "Po-211": 0.0007424423301461693,
                "Po-214": 84.99649018398776,
                "Po-215": 0.26900084425583065,
                "Po-218": 85.01434319248591,
                "Ra-223": 0.26900062820528614,
                "Ra-226": 85.01434319228659,
                "Rn-218": 1.7002868638497185e-05,
                "Rn-219": 0.26900062820528614,
                "Rn-222": 85.0143431924858,
                "Th-227": 0.2652884195245263,
                "Th-230": 85.01431274847525,
                "Th-231": 0.26898810215560653,
                "Th-234": 85.00820732310407,
                "Tl-206": 0.00011383420610068998,
                "Tl-207": 0.26825840192571576,
                "Tl-210": 0.01785300849981999,
                "U-234": 85.01287846492669,
                "U-235": 0.2689881021544942,
                "U-238": 85.00820732184867,
            },
        )

        # Catch incorrect sig_fig or no SymPy data in decay dataset
        with self.assertRaises(ValueError):
            inv.decay(1e9, "y", sig_fig=0)
        data = DecayData("icrp107", load_sympy=False)
        inv = Inventory({"H-3": 10.0}, data=data)
        with self.assertRaises(ValueError):
            inv.decay(1e9, "y", sig_fig=320)

    def test_inventory_decay_high_precision(self):
        """
        Test Inventory decay_high_precision() calculations.
        """
        inv = Inventory({"U-238": 99.274, "U-235": 0.720, "U-234": 0.005})
        self.assertEqual(
            inv.decay_high_precision(1e9, "y").contents,
            {
                "Ac-227": 0.26900062817405557,
                "At-218": 0.01700286863849718,
                "At-219": 2.227325201281318e-07,
                "Bi-210": 85.01434361515662,
                "Bi-211": 0.2690008442558584,
                "Bi-214": 85.01432618961894,
                "Bi-215": 2.1605054452429227e-07,
                "Fr-223": 0.003712208668802187,
                "Hg-206": 1.6152725286830195e-06,
                "Pa-231": 0.2690006198549054,
                "Pa-234": 0.13601313171698984,
                "Pa-234m": 85.00820732310412,
                "Pb-210": 85.01434361489547,
                "Pb-211": 0.26900084425585685,
                "Pb-214": 84.99734032384836,
                "Po-210": 85.01434362236536,
                "Po-211": 0.0007424423301461693,
                "Po-214": 84.99649018398776,
                "Po-215": 0.26900084425583065,
                "Po-218": 85.0143431924859,
                "Ra-223": 0.2690006282052861,
                "Ra-226": 85.0143431922866,
                "Rn-218": 1.7002868638497178e-05,
                "Rn-219": 0.26900062820528614,
                "Rn-222": 85.01434319248578,
                "Th-227": 0.26528841952452625,
                "Th-230": 85.01431274847525,
                "Th-231": 0.26898810215560653,
                "Th-234": 85.00820732310407,
                "Tl-206": 0.00011383420610068996,
                "Tl-207": 0.2682584019257157,
                "Tl-210": 0.017853008499819988,
                "U-234": 85.01287846492669,
                "U-235": 0.26898810215449415,
                "U-238": 85.00820732184867,
            },
        )

    def test_inventory_half_lives(self):
        """
        Test method to fetch half-lives of radionuclides in the Inventory.
        """

        inv = Inventory({"C-14": 1.0, "H-3": 2.0})
        self.assertEqual(inv.half_lives("y"), {"C-14": 5700.0, "H-3": 12.32})
        self.assertEqual(
            inv.half_lives("readable"), {"C-14": "5.70 ky", "H-3": "12.32 y"}
        )

    def test_inventory_progeny(self):
        """
        Test method to fetch progeny of radionuclides in the Inventory.
        """

        inv = Inventory({"C-14": 1.0, "K-40": 2.0})
        self.assertEqual(inv.progeny(), {"C-14": ["N-14"], "K-40": ["Ca-40", "Ar-40"]})

    def test_inventory_branching_fractions(self):
        """
        Test method to fetch branching fractions of radionuclides in the Inventory.
        """

        inv = Inventory({"C-14": 1.0, "K-40": 2.0})
        self.assertEqual(
            inv.branching_fractions(), {"C-14": [1.0], "K-40": [0.8914, 0.1086]}
        )

    def test_inventory_decay_modes(self):
        """
        Test method to fetch decay modes of radionuclides in the Inventory.
        """

        inv = Inventory({"C-14": 1.0, "K-40": 2.0})
        self.assertEqual(
            inv.decay_modes(),
            {"C-14": ["\u03b2-"], "K-40": ["\u03b2-", "\u03b2+ \u0026 EC"]},
        )

    @patch("matplotlib.pyplot.show")
    def test_inventory_plot(self, mock_show):
        """
        Test method to create decay plots.
        """

        inv = Inventory({"C-14": 1.0, "K-40": 2.0})
        _, ax = inv.plot(105, "ky")
        self.assertEqual(ax.get_xscale(), "linear")
        self.assertEqual(ax.get_yscale(), "linear")
        self.assertEqual(ax.get_xlabel(), "Time (ky)")
        self.assertEqual(ax.get_ylabel(), "Activity")
        self.assertEqual(ax.get_xlim(), (-5.25, 110.25))
        self.assertEqual(ax.get_ylim(), (0.0, 2.1))
        self.assertEqual(ax.get_legend_handles_labels()[-1], ["K-40", "C-14"])

        _, ax = inv.plot(
            100,
            xscale="log",
            yscale="log",
            yunits="Bq",
            sig_fig=320,
            display=["K40", "C14"],
        )
        self.assertEqual(ax.get_xscale(), "log")
        self.assertEqual(ax.get_yscale(), "log")
        self.assertEqual(ax.get_xlabel(), "Time (s)")
        self.assertEqual(ax.get_ylabel(), "Activity (Bq)")
        self.assertEqual(ax.get_xlim()[0], 0.0707945784384138)
        self.assertEqual(ax.get_ylim(), (0.1, 2.1))
        self.assertEqual(ax.get_legend_handles_labels()[-1], ["K-40", "C-14"])

        _, ax = inv.plot(100, "ky", xmin=50, ymin=1.0, ymax=2.5, display="K40")
        self.assertEqual(ax.get_xlim(), (47.5, 102.5))
        self.assertEqual(ax.get_ylim(), (1.0, 2.5))
        self.assertEqual(ax.get_legend_handles_labels()[-1], ["K-40"])

        _, ax = inv.plot(100, "ky", order="alphabetical")
        self.assertEqual(ax.get_legend_handles_labels()[-1], ["C-14", "K-40"])

        with self.assertRaises(ValueError):
            inv.plot(100, "ky", order="invalid")

    def test_inventory___repr__(self):
        """
        Test Inventory representations.
        """

        inv = Inventory({"H-3": 10.0})
        self.assertEqual(
            inv.__repr__(), "Inventory: {'H-3': 10.0}, decay dataset: icrp107"
        )

    def test_inventory___eq__(self):
        """
        Test Inventory equality.
        """

        inv1 = Inventory({"H-3": 10.0})
        inv2 = Inventory({"H3": 10.0})
        self.assertEqual(inv1, inv2)

        data = DecayData("icrp107")
        inv2 = Inventory({"H-3": 10.0}, data)
        self.assertEqual(inv1, inv2)

    def test_inventory___ne__(self):
        """
        Test Inventory not equality.
        """

        inv1 = Inventory({"H-3": 10.0})
        inv2 = Inventory({"Cs-137": 10.0})
        self.assertNotEqual(inv1, inv2)

        inv1 = Inventory({"H-3": 10.0})
        inv2 = Inventory({"H-3": 5.0})
        self.assertNotEqual(inv1, inv2)


if __name__ == "__main__":
    unittest.main()
