'''
Defines class containing data for radionuclide decay chain calculations.
Imports the decay data from files contained in the package.
'''

import numpy as np
from scipy import sparse
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

class DecayData:
    '''Stores data for radioactive decay calculations'''
    def __init__(self, dataset='icrp107'):
        self.dataset = dataset
        self.load_data()

    def get_path(self, filename):
        '''Get path of file to open'''
        with pkg_resources.path(__package__+'.'+self.dataset, filename) as path:
            return path

    def load_data(self):
        '''Read from files containing nuclear data'''
        self.matrix_c = sparse.load_npz(self.get_path('c.npz'))
        self.matrix_c_inv = sparse.load_npz(self.get_path('cinverse.npz'))
        self.no_nuclides = self.matrix_c.get_shape()[0]

        self.nuclide_dict = {}
        self.nuclide_names = []
        self.decay_consts = np.zeros([self.no_nuclides], dtype=np.float64)

        file_key = open(self.get_path('radionuclide_key.csv'), 'r')
        for i in range(0, self.no_nuclides):
            line = file_key.readline().split(',')
            nuclide_name = line[1].rstrip()
            self.nuclide_dict[nuclide_name] = int(line[0])
            self.nuclide_names.append(nuclide_name)
            self.decay_consts[i] = float(line[2])
        file_key.close()
