'''
Unit tests to check the functionality of the Python radioactivedecay package
'''

import unittest
import radioactivedecay as rd

class Test(unittest.TestCase):
    '''
    Unit tests for radioactivedecay functions, classes and methods.
    '''

    def test_parse_nuclide_name(self):
        '''
        Test the parsing of radionuclide strings
        '''

        # Re-formatting of acceptable strings e.g. 100Pd -> Pd-100
        self.assertEqual(rd.parse_nuclide_name('H-3', rd.DEFAULTDATA), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('H3', rd.DEFAULTDATA), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('3H', rd.DEFAULTDATA), 'H-3')
        self.assertEqual(rd.parse_nuclide_name('Be-7', rd.DEFAULTDATA), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('Be7', rd.DEFAULTDATA), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('7Be', rd.DEFAULTDATA), 'Be-7')
        self.assertEqual(rd.parse_nuclide_name('C-10', rd.DEFAULTDATA), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('C10', rd.DEFAULTDATA), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('10C', rd.DEFAULTDATA), 'C-10')
        self.assertEqual(rd.parse_nuclide_name('Ne-19', rd.DEFAULTDATA), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('Ne19', rd.DEFAULTDATA), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('19Ne', rd.DEFAULTDATA), 'Ne-19')
        self.assertEqual(rd.parse_nuclide_name('I-118', rd.DEFAULTDATA), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('I118', rd.DEFAULTDATA), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('118I', rd.DEFAULTDATA), 'I-118')
        self.assertEqual(rd.parse_nuclide_name('Pd-100', rd.DEFAULTDATA), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('Pd100', rd.DEFAULTDATA), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('100Pd', rd.DEFAULTDATA), 'Pd-100')
        self.assertEqual(rd.parse_nuclide_name('Cl-34m', rd.DEFAULTDATA), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('Cl34m', rd.DEFAULTDATA), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('34mCl', rd.DEFAULTDATA), 'Cl-34m')
        self.assertEqual(rd.parse_nuclide_name('I-118m', rd.DEFAULTDATA), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('I118m', rd.DEFAULTDATA), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('118mI', rd.DEFAULTDATA), 'I-118m')
        self.assertEqual(rd.parse_nuclide_name('Tb-156m', rd.DEFAULTDATA), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('Tb156m', rd.DEFAULTDATA), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('156mTb', rd.DEFAULTDATA), 'Tb-156m')
        self.assertEqual(rd.parse_nuclide_name('Tb-156n', rd.DEFAULTDATA), 'Tb-156n')
        self.assertEqual(rd.parse_nuclide_name('Tb156n', rd.DEFAULTDATA), 'Tb-156n')
        self.assertEqual(rd.parse_nuclide_name('156nTb', rd.DEFAULTDATA), 'Tb-156n')

       # Catch erroneous strings
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('A1', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('1A', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H-4', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('H4', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('4H', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('Pb-198m', rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.parse_nuclide_name('Pbo-198m', rd.DEFAULTDATA)

    def test_check_dictionary(self):
        '''
        Test the checking of inventory dictionaries
        '''

        # Dictionary parsing
        self.assertEqual(rd.check_dictionary({'H-3': 1.0}, rd.DEFAULTDATA), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H3': 1.0}, rd.DEFAULTDATA), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'3H': 1.0}, rd.DEFAULTDATA), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1}, rd.DEFAULTDATA), {'H-3': 1})
        self.assertEqual(rd.check_dictionary({'H-3': 1}, rd.DEFAULTDATA), {'H-3': 1.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1.0, 'C-14': 2.0}, rd.DEFAULTDATA),
                         {'H-3': 1.0, 'C-14': 2.0})
        self.assertEqual(rd.check_dictionary({'H-3': 1.0, 'C-14': 2.0}, rd.DEFAULTDATA),
                         {'C-14': 2.0, 'H-3': 1.0})

        # Catch incorrect activities
        with self.assertRaises(ValueError):
            rd.check_dictionary({'H-3': '1.0'}, rd.DEFAULTDATA)
        with self.assertRaises(ValueError):
            rd.check_dictionary({'1.0': 'H-3'}, rd.DEFAULTDATA)

    def test_time_unit_conv(self):
        '''
        Test function which converts between different time units
        '''

        # Check to and from seconds
        self.assertEqual(rd.time_unit_conv(1.0, 's', 's', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'us', rd.DEFAULTDATA), 1.0E6)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'ms', rd.DEFAULTDATA), 1.0E3)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'm', rd.DEFAULTDATA), 1.0/60.0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'h', rd.DEFAULTDATA), 1.0/(60.0**2))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'd', rd.DEFAULTDATA), 1.0/(60.0**2*24.0))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'y', rd.DEFAULTDATA),
                         1.0/(60.0**2*24.0*365.2422))
        self.assertEqual(rd.time_unit_conv(1.0, 's', 's', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'us', 's', rd.DEFAULTDATA), 1.0E-6)
        self.assertEqual(rd.time_unit_conv(1.0, 'ms', 's', rd.DEFAULTDATA), 1.0E-3)
        self.assertEqual(rd.time_unit_conv(1.0, 'm', 's', rd.DEFAULTDATA), 60.0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 's', rd.DEFAULTDATA), (60.0**2))
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 's', rd.DEFAULTDATA), (60.0**2*24.0))
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 's', rd.DEFAULTDATA), (60.0**2*24.0*365.2422))

        # Check variations and prefixed years
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'sec', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'second', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 's', 'seconds', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hr', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hour', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'h', 'hours', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 'day', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'd', 'days', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'yr', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'year', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'y', 'years', rd.DEFAULTDATA), 1.0E0)
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'ky', rd.DEFAULTDATA), 1.0E-3,
                               places=(3+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'My', rd.DEFAULTDATA), 1.0E-6,
                               places=(6+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Gy', rd.DEFAULTDATA), 1.0E-9,
                               places=(9+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Ty', rd.DEFAULTDATA), 1.0E-12,
                               places=(12+15))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'y', 'Py', rd.DEFAULTDATA), 1.0E-15,
                               places=(15+15))
        self.assertEqual(rd.time_unit_conv(1.0, 'sec', 's', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'second', 's', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'seconds', 's', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hr', 'h', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hour', 'h', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'hours', 'h', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'day', 'd', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'days', 'd', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'yr', 'y', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'year', 'y', rd.DEFAULTDATA), 1.0E0)
        self.assertEqual(rd.time_unit_conv(1.0, 'years', 'y', rd.DEFAULTDATA), 1.0E0)
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'ky', 'y', rd.DEFAULTDATA), 1.0E3,
                               places=(15-3))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'My', 'y', rd.DEFAULTDATA), 1.0E6,
                               places=(15-6))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Gy', 'y', rd.DEFAULTDATA), 1.0E9,
                               places=(15-9))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Ty', 'y', rd.DEFAULTDATA), 1.0E12,
                               places=(15-12))
        self.assertAlmostEqual(rd.time_unit_conv(1.0, 'Py', 'y', rd.DEFAULTDATA),
                               1.0E15, places=(15-15))

        # Catch incorrect time units
        with self.assertRaises(ValueError):
            rd.time_unit_conv(1.0, 'ty', 'y', rd.DEFAULTDATA)
            rd.time_unit_conv(1.0, 'y', 'ty', rd.DEFAULTDATA)
            rd.time_unit_conv(1.0, 'ty', 1.0, rd.DEFAULTDATA)

    def test_add_dictionaries(self):
        '''
        Test function which adds radioactivities together of two inventory dictionaries
        '''

        dict1 = {'Pm-141': 1.0, 'Rb-78': 2.0}
        dict2 = {'Pm-141': 3.0, 'Rb-90': 4.0}
        self.assertEqual(rd.add_dictionaries(dict1, dict2), {'Pm-141': 4.0, 'Rb-78': 2.0,
                                                             'Rb-90': 4.0})

if __name__ == '__main__':
    unittest.main()
