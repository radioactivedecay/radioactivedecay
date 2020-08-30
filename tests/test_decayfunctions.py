'''
Unit tests for decayfunctions.py functions, classes and methods.
'''

import copy
import unittest
import radioactivedecay as rd

class Test(unittest.TestCase):
    '''
    Unit tests for decayfunctions.py functions, classes and methods.
    '''

    def test_parse_nuclide_name(self):
        '''
        Test the parsing of radionuclide strings.
        '''

        nuclide_names = rd.DEFAULTDATA.nuclide_names
        dataset = rd.DEFAULTDATA.dataset

        # Re-formatting of acceptable strings e.g. 100Pd -> Pd-100
        self.assertEqual(rd.parse_nuclide_name('H-3', nuclide_names, dataset), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('H3', nuclide_names, dataset), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('3H', nuclide_names, dataset), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('Be-7', nuclide_names, dataset), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('Be7', nuclide_names, dataset), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('7Be', nuclide_names, dataset), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('C-10', nuclide_names, dataset), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('C10', nuclide_names, dataset), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('10C', nuclide_names, dataset), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('Ne-19', nuclide_names, dataset), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('Ne19', nuclide_names, dataset), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('19Ne', nuclide_names, dataset), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('I-118', nuclide_names, dataset), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('I118', nuclide_names, dataset), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('118I', nuclide_names, dataset), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('Pd-100', nuclide_names, dataset), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('Pd100', nuclide_names, dataset), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('100Pd', nuclide_names, dataset), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('Cl-34m', nuclide_names, dataset), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('Cl34m', nuclide_names, dataset), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('34mCl', nuclide_names, dataset), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('I-118m', nuclide_names, dataset), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('I118m', nuclide_names, dataset), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('118mI', nuclide_names, dataset), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('Tb-156m', nuclide_names, dataset), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('Tb156m', nuclide_names, dataset), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('156mTb', nuclide_names, dataset), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('Tb-156n', nuclide_names, dataset), 'Tb-156n')
        self.assertEqual(rd.parse_nuclide_name('Tb156n', nuclide_names, dataset), 'Tb-156n')
        self.assertEqual(rd.parse_nuclide_name('156nTb', nuclide_names, dataset), 'Tb-156n')

       # Catch erroneous strings
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('A1', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('1A', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H-4', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H4', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('4H', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('Pb-198m', nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('Pbo-198m', nuclide_names, dataset)

    def test_check_dictionary(self):
        '''
        Test the checking of inventory dictionaries.
        '''

        nuclide_names = rd.DEFAULTDATA.nuclide_names
        dataset = rd.DEFAULTDATA.dataset

        # Dictionary parsing
        self.assertEqual(rd.check_dictionary({'H-3': 1.0}, nuclide_names, dataset), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H3': 1.0}, nuclide_names, dataset), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'3H': 1.0}, nuclide_names, dataset), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1}, nuclide_names, dataset), {'H-3': 1})
        self.assertEqual(rd.check_dictionary({'H-3': 1}, nuclide_names, dataset), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1.0, 'C-14': 2.0}, nuclide_names, dataset),
                         {'H-3': 1.0, 'C-14': 2.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1.0, 'C-14': 2.0}, nuclide_names, dataset),
                         {'C-14': 2.0, 'H-3': 1.0})

        # Catch incorrect arguments
        with self.assertRaises(ValueError):
            rd.check_dictionary({'H-3': '1.0'}, nuclide_names, dataset)
        with self.assertRaises(ValueError):
            rd.check_dictionary({'1.0': 'H-3'}, nuclide_names, dataset)

    def test_time_unit_conv_seconds(self):
        '''
        Test function which converts between seconds and different time units.
        '''

        year_conv = rd.DEFAULTDATA.year_conv

        self.assertEqual(rd.time_unit_conv(1.0, 's', 's', year_conv), 1.0E0)
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 's', 'ns', year_conv), 1.0E9, places=(15-9))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'us', year_conv), 1.0E6)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'ms', year_conv), 1.0E3)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'm', year_conv), 1.0/60.0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'h', year_conv), 1.0/(60.0**2))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'd', year_conv), 1.0/(60.0**2*24.0))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'y', year_conv), 1.0/(60.0**2*24.0*365.2422))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'ns', 's', year_conv), 1.0E-9, places=(9+15))
        self.assertEqual(rd.time_unit_conv(1.0, 'us', 's', year_conv), 1.0E-6)
        self.assertEqual(rd.time_unit_conv(1.0, 'ms', 's', year_conv), 1.0E-3)
        self.assertEqual(rd.time_unit_conv(1.0, 'm', 's', year_conv), 60.0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 's', year_conv), (60.0**2))
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 's', year_conv), (60.0**2*24.0))
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 's', year_conv), (60.0**2*24.0*365.2422))

        # Catch some incorrect time units
        with self.assertRaises(ValueError):
            rd.time_unit_conv(1.0, 'ty', 'y', year_conv)
        with self.assertRaises(ValueError):
            rd.time_unit_conv(1.0, 'y', 'ty', year_conv)
        with self.assertRaises(ValueError):
            rd.time_unit_conv(1.0, 'ty', 1.0, year_conv)

    def test_time_unit_conv_spelling_variations(self):
        '''
        Test function which converts between spelling variations of different time units.
        '''

        year_conv = rd.DEFAULTDATA.year_conv

        self.assertEqual(rd.time_unit_conv(1.0, 's', 'sec', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'second', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'seconds', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hr', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hour', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hours', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 'day', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 'days', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'yr', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'year', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'years', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'sec', 's', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'second', 's', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'seconds', 's', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hr', 'h', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hour', 'h', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hours', 'h', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'day', 'd', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'days', 'd', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'yr', 'y', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'year', 'y', year_conv), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'years', 'y', year_conv), 1.0E0)

    def test_time_unit_conv_year_prefixes(self):
        '''
        Test function which converts between different year prefixes.
        '''

        year_conv = rd.DEFAULTDATA.year_conv

        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'ky', year_conv), 1.0E-3, places=(3+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'My', year_conv), 1.0E-6, places=(6+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Gy', year_conv), 1.0E-9, places=(9+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Ty', year_conv),
                               1.0E-12, places=(12+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Py', year_conv),
                               1.0E-15, places=(15+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'ky', 'y', year_conv), 1.0E3, places=(15-3))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'My', 'y', year_conv), 1.0E6, places=(15-6))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Gy', 'y', year_conv), 1.0E9, places=(15-9))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Ty', 'y', year_conv), 1.0E12,
                               places=(15-12))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Py', 'y', year_conv),
                               1.0E15, places=(15-15))

    def test_add_dictionaries(self):
        '''
        Test function which adds two inventory dictionaries together.
        '''

        dict1 = {'Pm-141': 1.0, 'Rb-78': 2.0}
        dict2 = {'Pm-141': 3.0, 'Rb-90': 4.0}
        self.assertEqual(rd.add_dictionaries(dict1, dict2), {'Pm-141': 4.0, 'Rb-78': 2.0,
                                                             'Rb-90': 4.0})

    def test_inventory_instantiation(self):
        '''
        Test instantiation of Inventory objects.
        '''

        inv = rd.Inventory({'H-3': 1.0})
        self.assertEqual(inv.contents, {'H-3': 1.0})
        inv = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
        self.assertEqual(inv.contents, {'Tc-99m': 2.3, 'I-123': 5.8})

    def test_inventory_change(self):
        '''
        Test Inventory change() method.
        '''

        inv = rd.Inventory({'H-3': 1.0})
        inv.change({'Tc-99m': 2.3, 'I-123': 5.8}, True, rd.DEFAULTDATA)
        self.assertEqual(inv.contents, {'Tc-99m': 2.3, 'I-123': 5.8})

    def test_inventory_radionuclides(self):
        '''
        Test Inventory radionuclides property.
        '''

        inv = rd.Inventory({'H-3': 1.0})
        self.assertEqual(inv.radionuclides, ['H-3'])
        inv = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
        self.assertEqual(inv.radionuclides, ['I-123', 'Tc-99m'])

    def test_inventory_activities(self):
        '''
        Test Inventory activities property.
        '''

        inv = rd.Inventory({'H-3': 1})
        self.assertEqual(inv.activities, [1.0])
        inv = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
        self.assertEqual(inv.activities, [5.8, 2.3])

    def test_inventory_add(self):
        '''
        Test Inventory add() method to append to an inventory.
        '''

        inv = rd.Inventory({'H-3': 1})
        inv.add({'C-14': 3.0, 'K-40': 4.0})
        self.assertEqual(inv.contents, {'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0})
        inv.add({'H-3': 3.0})
        self.assertEqual(inv.contents, {'C-14': 3.0, 'H-3': 4.0, 'K-40': 4.0})

    def test_inventory_subtract(self):
        '''
        Test Inventory subtract() method to take away a dictionary from an inventory.
        '''

        inv = rd.Inventory({'C-14': 3.0, 'H-3': 4.0, 'K-40': 4.0})
        inv.subtract({'C-14': 3.0, 'K-40': 4.0})
        self.assertEqual(inv.contents, {'C-14': 0.0, 'H-3': 4.0, 'K-40': 0.0})

    def test_inventory___add__(self):
        '''
        Test operator to add two inventory objects together.
        '''

        inv1 = rd.Inventory({'H-3': 1.0})
        inv2 = rd.Inventory({'C-14': 1.0, 'H-3': 4.0})
        inv = inv1 + inv2
        self.assertEqual(inv.contents, {'C-14': 1.0, 'H-3': 5.0})

        temp_data = copy.deepcopy(rd.DEFAULTDATA)
        temp_data.dataset = 'icrp107_'
        inv3 = rd.Inventory({'H-3': 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 + inv3

    def test_inventory___subtract__(self):
        '''
        Test operator to subtract one inventory object from another.
        '''

        inv1 = rd.Inventory({'H-3': 1.0})
        inv2 = rd.Inventory({'C-14': 1.0, 'H-3': 4.0})
        inv = inv2 - inv1
        self.assertEqual(inv.contents, {'C-14': 1.0, 'H-3': 3.0})

        temp_data = copy.deepcopy(rd.DEFAULTDATA)
        temp_data.dataset = 'icrp107_'
        inv3 = rd.Inventory({'H-3': 2.0}, data=temp_data)
        with self.assertRaises(ValueError):
            inv = inv1 - inv3

    def test_inventory___mul__(self):
        '''
        Test operator to multiply activities in inventory by constant.
        '''

        inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0})
        inv = inv * 2
        self.assertEqual(inv.contents, {'Cs-137': 2.0, 'Sr-90': 2.0})

    def test_inventory___rmul__(self):
        '''
        Test operator to right multiply constant by activities in inventory.
        '''

        inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0})
        inv = 2* inv
        self.assertEqual(inv.contents, {'Cs-137': 2.0, 'Sr-90': 2.0})

    def test_inventory___truediv__(self):
        '''
        Test operator to multiply activities in inventory by constant.
        '''

        inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0})
        inv = inv / 2
        self.assertEqual(inv.contents, {'Cs-137': 0.5, 'Sr-90': 0.5})

    def test_inventory_remove(self):
        '''
        Test operator to remove radionuclides from an inventory.
        '''

        inv = rd.Inventory({'C-14': 3.0, 'H-3': 4.0, 'K-40': 4.0})
        with self.assertRaises(NotImplementedError):
            inv.remove(1.0)

    def test_inventory_remove_string(self):
        '''
        Test operator to remove one radionuclide from an inventory.
        '''

        inv = rd.Inventory({'C-14': 3.0, 'H-3': 4.0, 'K-40': 4.0})
        inv.remove('H-3')
        self.assertEqual(inv.contents, {'C-14': 3.0, 'K-40': 4.0})

        with self.assertRaises(ValueError):
            inv.remove('Be-10')

    def test_inventory_remove_list(self):
        '''
        Test operator to remove list of radionuclides from an inventory.
        '''

        inv = rd.Inventory({'C-14': 3.0, 'H-3': 4.0, 'K-40': 4.0})
        inv.remove(['H-3', 'C-14'])
        self.assertEqual(inv.contents, {'K-40': 4.0})

        with self.assertRaises(ValueError):
            inv.remove(['Be-10', 'C-14'])

    def test_inventory_decay(self):
        '''
        Test Inventory decay() calculations.
        '''

        inv = rd.Inventory({'H-3': 10.0})
        self.assertEqual(inv.decay(12.32, 'y').contents, {'H-3': 5.0})
        inv = rd.Inventory({'Tc-99m': 2.3, 'I-123': 5.8})
        self.assertEqual(inv.decay(20.0, 'h').contents, {'I-123': 2.040459244534774,
                                                         'Tc-99': 6.729944738772211e-09,
                                                         'Tc-99m': 0.22950748010063513,
                                                         'Te-123': 9.485166535243877e-18,
                                                         'Te-123m': 7.721174031572363e-07})
        inv = rd.Inventory({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005})
        self.assertEqual(inv.decay(1E9, 'y').contents, {'Ac-227': 0.2690006281740556,
                                                        'At-218': 0.017002868638497183,
                                                        'At-219': 2.227325201281319e-07,
                                                        'Bi-210': 85.01434361515662,
                                                        'Bi-211': 0.26900084425585846,
                                                        'Bi-214': 85.01432618961896,
                                                        'Bi-215': 2.1605054452429237e-07,
                                                        'Fr-223': 0.0037122086688021884,
                                                        'Hg-206': 1.6152725286830197e-06,
                                                        'Pa-231': 0.2690006198549055,
                                                        'Pa-234': 0.13601313171698984,
                                                        'Pa-234m': 85.00820732310412,
                                                        'Pb-210': 85.01434361489548,
                                                        'Pb-211': 0.2690008442558569,
                                                        'Pb-214': 84.99734032384839,
                                                        'Po-210': 85.01434362236536,
                                                        'Po-211': 0.0007424423301461693,
                                                        'Po-214': 84.99649018398776,
                                                        'Po-215': 0.26900084425583065,
                                                        'Po-218': 85.01434319248591,
                                                        'Ra-223': 0.26900062820528614,
                                                        'Ra-226': 85.01434319228659,
                                                        'Rn-218': 1.7002868638497185e-05,
                                                        'Rn-219': 0.26900062820528614,
                                                        'Rn-222': 85.0143431924858,
                                                        'Th-227': 0.2652884195245263,
                                                        'Th-230': 85.01431274847525,
                                                        'Th-231': 0.26898810215560653,
                                                        'Th-234': 85.00820732310407,
                                                        'Tl-206': 0.00011383420610068998,
                                                        'Tl-207': 0.26825840192571576,
                                                        'Tl-210': 0.01785300849981999,
                                                        'U-234': 85.01287846492669,
                                                        'U-235': 0.2689881021544942,
                                                        'U-238': 85.00820732184867})

    def test_inventory___repr__(self):
        '''
        Test Inventory representations.
        '''

        inv = rd.Inventory({'H-3': 10.0})
        self.assertEqual(inv.__repr__(), 'Inventory: {\'H-3\': 10.0}, Decay dataset: icrp107')

    def test_radionuclide_instantiation(self):
        '''
        Test instantiation of Radionuclide objects.
        '''

        nuc = rd.Radionuclide('H-3')
        self.assertEqual(nuc.nuclide_name, 'H-3')

    def test_radionuclide_change(self):
        '''
        Test Radionuclide change() method.
        '''

        nuc = rd.Radionuclide('H-3')
        nuc.change('Rn-222', rd.DEFAULTDATA)
        self.assertEqual(nuc.nuclide_name, 'Rn-222')
        self.assertEqual(nuc.decay_constant, 2.0982180755947176e-06)

    def test_radionuclide_half_life(self):
        '''
        Test Radionuclide half_life() method.
        '''

        nuc = rd.Radionuclide('H-3')
        self.assertEqual(nuc.half_life('y'), 12.32)

    def test_radionuclide___repr__(self):
        '''
        Test Radionuclide representations.
        '''

        nuc = rd.Radionuclide('H-3')
        self.assertEqual(nuc.__repr__(), 'Radionuclide: H-3, Decay dataset: icrp107')

if __name__ == '__main__':
    unittest.main()
