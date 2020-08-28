'''
The decacydata module defines the ``DecayData`` class. Instances of ``DecayData`` initalize by
reading in dataset files containing radioactive decay data. The objects then store the data for
various uses, such as decay calculations and reporting radionuclide decay data.
'''

import numpy as np
from scipy import sparse
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

class DecayData:
    '''
    Instances of DecayData store a radioactive decay dataset.

    Parameters
    ----------
    dataset : str
        Name of the radioactivedecay dataset.
    path : str or None, optional
        Path to folder containing the decay dataset files. Use None if the data are bundled as a
        sub-package of ``radioactivedecay`` (default is None).

    Attributes
    ----------
    dataset : str
        Name of the radioactivedecay dataset.
    decay_consts : numpy.ndarray
        NumPy array of radionuclide decay constants.
    matrix_c : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a lower traingular matrix with constant elements that are precalculated from decay
        constants and branching fractions.
    matrix_c_inv : scipy.sparse.csc.csc_matrix
        The inverse of matrix_c.
    matrix_e : scipy.sparse.csc.csc_matrix
        SciPy Compressed Sparse Column (CSC) matrix that is used in radioactive decay calculations.
        It is a diagonal matrix that is pre-allocted here for performance reasons.
    no_nuclides : int
        Number of radionuclides in the dataset.
    nuclide_names : numpy.ndarray
        NumPy array of radionuclide names.
    nuclide_dict : dict
        Dictionary containing radionuclide strings as keys and positions in the nuclide_names array
        as values.
    year_conv : float
        Conversion factor for number of days in one year.

    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self, dataset, path=None):
        self.dataset = dataset
        self.load_data(path)

    def get_path(self, filename):
        '''
        Returns path of file to open if the dataset is bundled as as sub-package of
        ``radioactivedecay``.
        '''

        with pkg_resources.path(__package__+'.'+self.dataset, filename) as package_path:
            return package_path

    def load_data(self, path):
        '''
        Reads in radioactive decay dataset files and puts the data into DecayData instance
        attributes.

        Parameters
        ----------
        path : str or None
            Path to folder containing the decay dataset files, or None if the data are bundled as a
            sub-package of ``radioactivedecay``.

        '''

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
