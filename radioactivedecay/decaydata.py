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
    # pylint: disable=too-many-instance-attributes
    def __init__(self, dataset='icrp107', path=None):
        self.dataset = dataset
        self.load_data(path)

    def get_path(self, filename):
        '''Get path of file to open'''
        with pkg_resources.path(__package__+'.'+self.dataset, filename) as package_path:
            return package_path

    def load_data(self, path):
        '''Read from files containing nuclear data'''
        if path is None:
            data = np.load(self.get_path('radionuclides_decay_consts.npz'))
        else:
            data = np.load(path+'/radionuclides_decay_consts.npz')
        self.nuclide_names = data['nuclide_names']
        self.decay_consts = data['decay_consts']
        self.year_conv = data['year_conv']

        self.no_nuclides = self.nuclide_names.size
        self.nuclide_dict = dict(zip(self.nuclide_names, list(range(0, self.no_nuclides))))
        self.matrix_e = sparse.csc_matrix((np.zeros(self.no_nuclides),
                                           (np.arange(self.no_nuclides),
                                            np.arange(self.no_nuclides))))

        if path is None:
            self.matrix_c = sparse.load_npz(self.get_path('c.npz'))
            self.matrix_c_inv = sparse.load_npz(self.get_path('cinverse.npz'))
        else:
            self.matrix_c = sparse.load_npz(path+'/c.npz')
            self.matrix_c_inv = sparse.load_npz(path+'/cinverse.npz')

    def __repr__(self):
        return 'Decay dataset: '+self.dataset
