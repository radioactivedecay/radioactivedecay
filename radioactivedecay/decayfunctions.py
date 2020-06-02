'''
Functions to perform radioactive decay calculations.
'''

import numpy as np
from scipy import sparse
import radioactivedecay.decaydata as decaydata

DEFAULTDATA = decaydata. DecayData('icrp107')

def parse_nuclide_name(nuclide_name, data):
    '''Parse radionuclide string and check for validity.'''

    letter_flag, number_flag = False, False
    for char in nuclide_name:
        if char.isalpha():
            letter_flag = True
        if char.isdigit():
            number_flag = True
        if letter_flag and number_flag:
            break

    if not (letter_flag and number_flag) or len(nuclide_name) < 2 or len(nuclide_name) > 7:
        raise ValueError(str(nuclide_name) + ' is not a valid radionuclide in decay dataset.')

    original_nuclide_name = nuclide_name

    while nuclide_name[0].isdigit():     # Re-order inputs e.g. 99mTc to Tc99m.
        nuclide_name = nuclide_name[1:]+nuclide_name[0]
    if nuclide_name[0] in ['m', 'n']:
        nuclide_name = nuclide_name[1:]+nuclide_name[0]

    for i in range(1, len(nuclide_name)):    # Add hyphen e.g. Tc99m to Tc-99m.
        if nuclide_name[i].isdigit():
            if nuclide_name[i-1] != '-':
                nuclide_name = nuclide_name[:i]+'-'+nuclide_name[i:]
            break

    if nuclide_name not in data.nuclide_names:
        raise ValueError(str(original_nuclide_name) + ' is not a valid radionuclide in decay '\
                         'dataset.')

    return nuclide_name

def check_dictionary(inv_dict, data):
    '''Check validity of python dictionary listing radionuclides and associated acitivities.'''

    for nuclide_name, activity in inv_dict.items():
        parsed_nuclide_name = parse_nuclide_name(nuclide_name, data)
        inv_dict[parsed_nuclide_name] = inv_dict.pop(nuclide_name)

        if not isinstance(activity, (float, int)):
            raise ValueError(str(activity) + " is not a valid radioactivity.")

    return True

def time_unit_conv(time, units, unitsto):
    '''Convert time to seconds.'''

    conv = {'s':1.0, 'm':60.0, 'h':3600.0, 'd':86400.0, 'y':31556952.0}

    if units not in conv:
        raise ValueError(str(units) + " is not a valid unit, e.g. s, m, h, d or y.")

    return time*conv[units]/conv[unitsto]

class Inventory:
    '''Inventory of multiple radionuclides and their associated activities.'''

    def __init__(self, contents, check=True, data=DEFAULTDATA):
        self.change(contents, check, data)

    def change(self, contents, check, data):
        '''Change contents of inventory to contents.'''
        if check is True:
            check_dictionary(contents, data)
        self.contents = dict(sorted(contents.items(), key=lambda x: x[0]))
        self.radionuclides = list(self.contents)
        self.activities = list(self.contents.values())
        self.data = data

    def decay(self, decay_time, units=None):
        '''Perform decay calculation of the inventory for period decay_time.'''
        decay_time = time_unit_conv(decay_time, units=units, unitsto='s') if units else decay_time

        vector_n0 = np.zeros([self.data.no_nuclides], dtype=np.float64)
        indices = set()
        for nuclide_name in self.contents:
            i = self.data.nuclide_dict[nuclide_name]
            vector_n0[i] = self.contents[nuclide_name]/self.data.decay_consts[i]
            indices.update(self.data.matrix_c[:, i].nonzero()[0])
        vector_l = self.data.decay_consts if i in indices else 0.0

        matrix_e = sparse.dia_matrix((np.exp(np.multiply(-1.0*decay_time, vector_l)),
                                      np.array([0])), shape=(self.data.no_nuclides,
                                                             self.data.no_nuclides))
        vector_nt = ((self.data.matrix_c.dot(matrix_e)).dot(self.data.matrix_c_inv)).dot(vector_n0)
        vector_at = np.multiply(vector_nt, vector_l)

        new_contents = {}
        for i in indices:
            new_contents[self.data.nuclide_names[i]] = vector_at[i]
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))
        return Inventory(new_contents, check=False)

class Radionuclide:
    '''Radionuclide, its half-life and its decay constant'''

    ln2 = np.log(2)

    def __init__(self, nuclide_name, data=DEFAULTDATA):
        self.change(nuclide_name, data)

    def change(self, nuclide_name, data):
        '''Change the radionuclide, fetch its data.'''
        self.nuclide_name = parse_nuclide_name(nuclide_name, data)
        self.decay_constant = data.decay_consts[data.nuclide_dict[self.nuclide_name]]
        self.half_life = Radionuclide.ln2/self.decay_constant

    def halflife(self, units=None):
        '''Return half life of radionuclide with user chosen units (default seconds).'''
        conv = time_unit_conv(1.0, 's', units) if units else 1.0
        return self.half_life*conv
