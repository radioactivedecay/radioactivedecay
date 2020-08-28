'''
Unit tests for decaydata.py functions, classes and methods.
'''

import unittest
from radioactivedecay import decaydata

class Test(unittest.TestCase):
    '''
    Unit tests for decaydata.py functions, classes and methods.
    '''

    def test_decaydata_instantiation(self):
        '''
        Test instantiation of DecayData objects.
        '''

        data = decaydata.DecayData('icrp107')
        self.assertEqual(data.dataset, 'icrp107')
        self.assertEqual(data.no_nuclides, 1252)
        self.assertEqual(data.year_conv, 365.2422)
        self.assertEqual(data.nuclide_names[0], 'Fm-257')
        self.assertEqual(data.nuclide_names[-1], 'H-3')
        self.assertEqual(data.decay_consts[0], 7.982623693568561e-08)
        self.assertEqual(data.decay_consts[-1], 1.7828715741004621e-09)
        self.assertEqual(data.nuclide_dict['Fm-257'], 0)
        self.assertEqual(data.nuclide_dict['H-3'], 1251)

    def test_decaydata___repr__(self):
        '''
        Test DecayData representations.
        '''

        data = decaydata.DecayData('icrp107')
        self.assertEqual(data.__repr__(), 'Decay dataset: icrp107')

if __name__ == '__main__':
    unittest.main()
