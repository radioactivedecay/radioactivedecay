"""
Unit tests for decayfunctions.py functions, classes and methods.
"""

import copy
import unittest
import radioactivedecay as rd


class Test(unittest.TestCase):
    """
    Unit tests for decayfunctions.py functions, classes and methods.
    """

    # pylint: disable=too-many-public-methods

    def test_inventory_instantiation(self):
        """
        Test instantiation of Inventory objects.
        """

        inv = rd.Inventory({"H-3": 1.0})
        self.assertEqual(inv.contents, {"H-3": 1.0})
        inv = rd.Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

    def test_inventory_change(self):
        """
        Test Inventory change() method.
        """

        inv = rd.Inventory({"H-3": 1.0})
        inv.change({"Tc-99m": 2.3, "I-123": 5.8}, True, rd.DEFAULTDATA)
        self.assertEqual(inv.contents, {"Tc-99m": 2.3, "I-123": 5.8})

    def test_inventory_radionuclides(self):
        """
        Test Inventory radionuclides property.
        """

        inv = rd.Inventory({"H-3": 1.0})
        self.assertEqual(inv.radionuclides, ["H-3"])
        inv = rd.Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.radionuclides, ["I-123", "Tc-99m"])

    def test_inventory_activities(self):
        """
        Test Inventory activities property.
        """

        inv = rd.Inventory({"H-3": 1})
        self.assertEqual(inv.activities, [1.0])
        inv = rd.Inventory({"Tc-99m": 2.3, "I-123": 5.8})
        self.assertEqual(inv.activities, [5.8, 2.3])

    def test_inventory_add(self):
        """
        Test Inventory add() method to append to an inventory.
        """

        inv = rd.Inventory({"H-3": 1})
        inv.add({"C-14": 3.0, "K-40": 4.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 1.0, "K-40": 4.0})
        inv.add({"H-3": 3.0})
        self.assertEqual(inv.contents, {"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})

    def test_inventory_subtract(self):
        """
        Test Inventory subtract() method to take away a dictionary from an inventory.
        """

        inv = rd.Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.subtract({"C-14": 3.0, "K-40": 4.0})
        self.assertEqual(inv.contents, {"C-14": 0.0, "H-3": 4.0, "K-40": 0.0})

    def test_inventory___add__(self):
        """
        Test operator to add two inventory objects together.
        """

        inv1 = rd.Inventory({"H-3": 1.0})
        inv2 = rd.Inventory({"C-14": 1.0, "H-3": 4.0})
        inv = inv1 + inv2
        self.assertEqual(inv.contents, {"C-14": 1.0, "H-3": 5.0})

        temp_data = copy.deepcopy(rd.DEFAULTDATA)
        temp_data.dataset = "icrp107_"
        inv3 = rd.Inventory({"H-3": 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 + inv3

    def test_inventory___subtract__(self):
        """
        Test operator to subtract one inventory object from another.
        """

        inv1 = rd.Inventory({"H-3": 1.0})
        inv2 = rd.Inventory({"C-14": 1.0, "H-3": 4.0})
        inv = inv2 - inv1
        self.assertEqual(inv.contents, {"C-14": 1.0, "H-3": 3.0})

        temp_data = copy.deepcopy(rd.DEFAULTDATA)
        temp_data.dataset = "icrp107_"
        inv3 = rd.Inventory({"H-3": 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 - inv3

    def test_inventory___mul__(self):
        """
        Test operator to multiply activities in inventory by constant.
        """

        inv = rd.Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = inv * 2
        self.assertEqual(inv.contents, {"Cs-137": 2.0, "Sr-90": 2.0})

    def test_inventory___rmul__(self):
        """
        Test operator to right multiply constant by activities in inventory.
        """

        inv = rd.Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = 2 * inv
        self.assertEqual(inv.contents, {"Cs-137": 2.0, "Sr-90": 2.0})

    def test_inventory___truediv__(self):
        """
        Test operator to multiply activities in inventory by constant.
        """

        inv = rd.Inventory({"Sr-90": 1.0, "Cs-137": 1.0})
        inv = inv / 2
        self.assertEqual(inv.contents, {"Cs-137": 0.5, "Sr-90": 0.5})

    def test_inventory_remove(self):
        """
        Test operator to remove radionuclides from an inventory.
        """

        inv = rd.Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        with self.assertRaises(NotImplementedError):
            inv.remove(1.0)

    def test_inventory_remove_string(self):
        """
        Test operator to remove one radionuclide from an inventory.
        """

        inv = rd.Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove("H-3")
        self.assertEqual(inv.contents, {"C-14": 3.0, "K-40": 4.0})

        with self.assertRaises(ValueError):
            inv.remove("Be-10")

    def test_inventory_remove_list(self):
        """
        Test operator to remove list of radionuclides from an inventory.
        """

        inv = rd.Inventory({"C-14": 3.0, "H-3": 4.0, "K-40": 4.0})
        inv.remove(["H-3", "C-14"])
        self.assertEqual(inv.contents, {"K-40": 4.0})

        with self.assertRaises(ValueError):
            inv.remove(["Be-10", "C-14"])

    def test_inventory_decay(self):
        """
        Test Inventory decay() calculations.
        """

        inv = rd.Inventory({"H-3": 10.0})
        self.assertEqual(inv.decay(12.32, "y").contents, {"H-3": 5.0})
        inv = rd.Inventory({"Tc-99m": 2.3, "I-123": 5.8})
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
        inv = rd.Inventory({"U-238": 99.274, "U-235": 0.720, "U-234": 0.005})
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

    def test_inventory___repr__(self):
        """
        Test Inventory representations.
        """

        inv = rd.Inventory({"H-3": 10.0})
        self.assertEqual(
            inv.__repr__(), "Inventory: {'H-3': 10.0}, Decay dataset: icrp107"
        )

    def test_radionuclide_instantiation(self):
        """
        Test instantiation of Radionuclide objects.
        """

        nuc = rd.Radionuclide("H-3")
        self.assertEqual(nuc.radionuclide, "H-3")

    def test_radionuclide_change(self):
        """
        Test Radionuclide change() method.
        """

        nuc = rd.Radionuclide("H-3")
        nuc.change("Rn-222", rd.DEFAULTDATA)
        self.assertEqual(nuc.radionuclide, "Rn-222")
        self.assertEqual(nuc.decay_constant, 2.0982180755947176e-06)

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
