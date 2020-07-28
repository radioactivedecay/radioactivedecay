'''
Functions and classes for radioactive decay calculations.
'''

from functools import singledispatch, update_wrapper
import numpy as np
import radioactivedecay.decaydata as decaydata

# Use ICRP-107 as default radioactive decay dataset
DEFAULTDATA = decaydata.DecayData('icrp107')

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
        raise ValueError(str(original_nuclide_name) + ' is not a valid radionuclide in '\
                         + data.dataset + ' dataset.')

    return nuclide_name

def check_dictionary(inv_dict, data):
    '''Check validity of python dictionary listing radionuclides and associated acitivities.'''

    inv_dict = {parse_nuclide_name(nuc, data): act for nuc, act in inv_dict.items()}
    for nuc, act in inv_dict.items():
        if not isinstance(act, (float, int)):
            raise ValueError(str(act) + ' is not a valid radioactivity for ' + str(nuc) + '.')

    return inv_dict

def time_unit_conv(time, units, unitsto):
    '''Convert between time units.'''

    conv = {'us':1.0E-6, 'ms':1.0E-3, 's':1.0, 'm':60.0, 'h':3600.0, 'd':86400.0, 'y':31556952.0,
            'sec':1, 'second':1, 'seconds':1, 'hr':3600.0, 'hour':3600.0, 'hours':3600.0,
            'day':86400.0, 'days':86400.0, 'yr':31556952.0, 'year':31556952.0, 'years':31556952.0,
            'ky':31556952.0E3, 'My':31556952.0E6, 'Gy':31556952.0E9, 'Ty':31556952.0E12,
            'Py':31556952.0E15}

    if units not in conv:
        raise ValueError(str(units) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".')
    if unitsto not in conv:
        raise ValueError(str(unitsto) + ' is not a valid unit, e.g. "s", "m", "h", "d" or "y".')

    return time*conv[units]/conv[unitsto]

def add_dictionaries(dict1, dict2):
    '''Add together two dictionaries of radionuclies and associated acitivities.'''

    new_dict = dict1.copy()
    for nuclide, radioactivity in dict2.items():
        if nuclide in new_dict:
            new_dict[nuclide] = new_dict[nuclide] + radioactivity
        else:
            new_dict[nuclide] = radioactivity

    return new_dict

def method_dispatch(func):
    '''Add singledispatch support for class methods.'''

    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

class Inventory:
    '''Inventory of radionuclides and their associated activities.'''

    def __init__(self, contents, check=True, data=DEFAULTDATA):
        self.change(contents, check, data)

    def change(self, contents, check, data):
        '''Change contents of inventory to contents.'''
        if check is True:
            contents = check_dictionary(contents, data)
        self.contents = dict(sorted(contents.items(), key=lambda x: x[0]))
        self.data = data

    @property
    def radionuclides(self):
        '''Return list of radionuclides in Inventory.'''
        return list(self.contents)

    @property
    def activities(self):
        '''Return list of activities in Inventory.'''
        return list(self.contents.values())

    def add(self, add_contents):
        '''Add a dictionary of radionuclides and associated activities to this inventory.'''
        add_contents = check_dictionary(add_contents, self.data)
        new_contents = add_dictionaries(self.contents, add_contents)
        self.change(new_contents, False, self.data)

    def subtract(self, sub_contents):
        '''Subtract a dictionary of radionuclides and associated activities from this inventory.'''
        sub_contents = check_dictionary(sub_contents, self.data)
        sub_contents.update((nuclide, radioactivity*-1.0) for nuclide, radioactivity in
                            sub_contents.items())
        new_contents = add_dictionaries(self.contents, sub_contents)
        self.change(new_contents, False, self.data)

    def __add__(self, other):
        '''Add two Inventory instances together.'''
        if self.data.dataset != other.data.dataset:
            raise ValueError('Decay datasets do not match. inv1: ' + self.data.dataset + ' inv2: '
                             + other.data.dataset)
        new_contents = add_dictionaries(self.contents, other.contents)
        return Inventory(new_contents, False, self.data)

    def __sub__(self, other):
        '''Subtract contents of one Inventory from another.'''
        if self.data.dataset != other.data.dataset:
            raise ValueError('Decay datasets do not match. inv1: ' + self.data.dataset + ' inv2: '
                             + other.data.dataset)
        sub_contents = other.contents.copy()
        sub_contents.update((nuclide, radioactivity*-1.0) for nuclide, radioactivity in
                            sub_contents.items())
        new_contents = add_dictionaries(self.contents, sub_contents)
        return Inventory(new_contents, False, self.data)

    @method_dispatch
    def remove(self, delete):
        '''Remove radionuclide(s) from this inventory.'''
        raise NotImplementedError('remove() takes string or list of radionuclides.')

    @remove.register(str)
    def _(self, delete):
        '''Remove radionuclide string from this inventory.'''
        delete = parse_nuclide_name(delete, self.data)
        new_contents = self.contents.copy()
        if delete not in new_contents:
            raise ValueError(delete + ' does not exist in this inventory.')
        new_contents.pop(delete)
        self.change(new_contents, False, self.data)

    @remove.register(list)
    def _(self, delete):
        '''Remove list of radionuclide(s) from this inventory.'''
        delete = [parse_nuclide_name(nuc, self.data) for nuc in delete]
        new_contents = self.contents.copy()
        for nuc in delete:
            if nuc not in new_contents:
                raise ValueError(nuc + ' does not exist in this inventory.')
            new_contents.pop(nuc)
        self.change(new_contents, False, self.data)

    def decay(self, decay_time, units=None):
        '''Perform decay calculation of the inventory for period decay_time.'''
        decay_time = time_unit_conv(decay_time, units=units, unitsto='s') if units else decay_time

        vector_n0 = np.zeros([self.data.no_nuclides], dtype=np.float64)
        indices = set()
        for nuclide_name in self.contents:
            i = self.data.nuclide_dict[nuclide_name]
            vector_n0[i] = self.contents[nuclide_name]/self.data.decay_consts[i]
            indices.update(self.data.matrix_c[:, i].nonzero()[0])
        indices = list(indices)

        matrix_e = self.data.matrix_e.copy()
        matrix_e.data[indices] = np.exp(np.multiply(-decay_time, self.data.decay_consts[indices]))
        vector_nt = ((self.data.matrix_c.dot(matrix_e)).dot(self.data.matrix_c_inv)).dot(vector_n0)
        vector_at = np.multiply(vector_nt, self.data.decay_consts)

        new_contents = dict(zip(self.data.nuclide_names[indices], vector_at[indices]))
        new_contents = dict(sorted(new_contents.items(), key=lambda x: x[0]))
        return Inventory(new_contents, False, self.data)

    def __repr__(self):
        return 'Inventory: '+str(self.contents)+', Decay dataset: '+self.data.dataset

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
        self.data = data

    def halflife(self, units=None):
        '''Return half life of radionuclide with user chosen units (default seconds).'''
        conv = time_unit_conv(1.0, units='s', unitsto=units) if units else 1.0
        return self.half_life*conv

    def __repr__(self):
        return 'Radionuclide: '+str(self.nuclide_name)+', Decay dataset: '+self.data.dataset
