"""
Unit tests for decaydata.py functions, classes and methods.
"""

import unittest
import numpy as np
from scipy import sparse
from sympy import Integer, log, Matrix
from sympy.matrices import SparseMatrix
from radioactivedecay import decaydata, icrp107


class Test(unittest.TestCase):
    """
    Unit tests for decaydata.py functions, classes and methods.
    """

    def test__csr_matrix_equal(self):
        """
        Test function to check equality of two SciPy Compressed Sparse Row (CSR) matrices.
        """

        matrix_a = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_b = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c = sparse.csr_matrix(([1.0], ([1], [0])), shape=(2, 2))
        self.assertEqual(decaydata._csr_matrix_equal(matrix_a, matrix_b), True)
        self.assertEqual(decaydata._csr_matrix_equal(matrix_a, matrix_c), False)

    def test_decaymatrices_instantiation(self):
        """
        Test instantiation of DecayMatrices objects.
        """

        # check with artificial SciPy data
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([1], [1])), shape=(2, 2))
        year_conv = 365.0
        decay_mats = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(decay_mats.decay_consts[0], 0.0)
        self.assertEqual(decay_mats.decay_consts[1], 0.0)
        self.assertEqual(decay_mats.ln2, np.log(2))
        self.assertEqual(decay_mats.matrix_c[0, 0], 1.0)
        self.assertEqual(decay_mats.matrix_c_inv[1, 1], 1.0)
        self.assertEqual(decay_mats.matrix_e[0, 0], 0.0)
        self.assertEqual(decay_mats.matrix_e[1, 1], 0.0)
        self.assertEqual(decay_mats.vector_n0[0], 0.0)
        self.assertEqual(decay_mats.vector_n0[1], 0.0)
        self.assertEqual(decay_mats.year_conv, year_conv)

        # check with artificial SymPy data
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        year_conv = Integer(36525) / Integer(365)
        decay_mats = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(decay_mats.decay_consts[0], 0.0)
        self.assertEqual(decay_mats.decay_consts[1], 0.0)
        self.assertEqual(decay_mats.ln2, log(2))
        self.assertEqual(decay_mats.matrix_c[0, 0], Integer(2))
        self.assertEqual(decay_mats.matrix_c_inv[1, 1], Integer(3))
        self.assertEqual(decay_mats.matrix_e[0, 0], Integer(0))
        self.assertEqual(decay_mats.matrix_e[1, 1], Integer(0))
        self.assertEqual(decay_mats.vector_n0[0], 0.0)
        self.assertEqual(decay_mats.vector_n0[1], 0.0)
        self.assertEqual(decay_mats.year_conv, Integer(36525) / Integer(365))

    def test_decaymatrices___eq__(self):
        """
        Test DecayMatrices instances equal.
        """

        # check with artificial SciPy data
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        year_conv = 365.0
        decay_mats_a = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        year_conv = 365.0
        decay_mats_b = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(decay_mats_a, decay_mats_b)

        # check with artificial SymPy data
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        year_conv = Integer(36525) / Integer(365)
        decay_mats_a = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        year_conv = Integer(36525) / Integer(365)
        decay_mats_b = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(decay_mats_a, decay_mats_b)

    def test_decaymatrices___ne__(self):
        """
        Test DecayMatrices instances not equal.
        """

        # check with artificial SciPy data
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        year_conv = 365.0
        decay_mats_a = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([2.0], ([0], [0])), shape=(2, 2))
        year_conv = 365.0
        decay_mats_b = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertNotEqual(decay_mats_a, decay_mats_b)

        # check with artificial SymPy data
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        year_conv = Integer(36525) / Integer(365)
        decay_mats_a = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(5)
        year_conv = Integer(36525) / Integer(365)
        decay_mats_b = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertNotEqual(decay_mats_a, decay_mats_b)

    def test_decaymatrices___repr__(self):
        """
        Test DecayMatrices representations.
        """

        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([1], [1])), shape=(2, 2))
        year_conv = 365.0
        decay_mats = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(
            decay_mats.__repr__(),
            "DecayMatrices: data stored in SciPy/NumPy objects for double precision calculations.",
        )

        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        year_conv = Integer(36525) / Integer(365)
        decay_mats = decaydata.DecayMatrices(
            decay_consts, matrix_c, matrix_c_inv, year_conv
        )
        self.assertEqual(
            decay_mats.__repr__(),
            "DecayMatrices: data stored in SymPy objects for arbitrary-precision calculations.",
        )

    def test_decaydata_instantiation(self):
        """
        Test instantiation of DecayData objects.
        """

        # pylint: disable=too-many-statements

        # check instantiation from sub-package
        data = decaydata.DecayData("icrp107", load_sympy=False)
        self.assertEqual(data.dataset, "icrp107")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], 12.32)
        self.assertEqual(data.hldata[-1][1], "y")
        self.assertEqual(data.num_radionuclides, 1252)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.scipy_data.year_conv, 365.2422)
        self.assertEqual(data.sympy_data, None)

        # check instantiation with supplied dataset path
        data = decaydata.DecayData("icrp107_2", icrp107.__path__[0], load_sympy=False)
        self.assertEqual(data.dataset, "icrp107_2")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], 12.32)
        self.assertEqual(data.hldata[-1][1], "y")
        self.assertEqual(data.num_radionuclides, 1252)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.scipy_data.year_conv, 365.2422)
        self.assertEqual(data.sympy_data, None)

        # check instantiation from sub-package with SymPy data
        data = decaydata.DecayData("icrp107", load_sympy=True)
        self.assertEqual(data.dataset, "icrp107")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], 12.32)
        self.assertEqual(data.hldata[-1][1], "y")
        self.assertEqual(data.num_radionuclides, 1252)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.scipy_data.year_conv, 365.2422)
        self.assertEqual(
            data.sympy_data.decay_consts[0],
            log(2) * Integer(10) / (Integer(1005) * Integer(24) * Integer(3600)),
        )
        self.assertEqual(data.sympy_data.ln2, log(2))
        self.assertEqual(data.sympy_data.matrix_c[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_c_inv[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_e[0, 0], Integer(0))
        self.assertEqual(data.sympy_data.vector_n0[0], Integer(0))
        self.assertEqual(data.sympy_data.year_conv, Integer(3652422) / Integer(10000))

        # check instantiation with supplied dataset path with SymPy data
        data = decaydata.DecayData("icrp107_2", icrp107.__path__[0], load_sympy=True)
        self.assertEqual(data.dataset, "icrp107_2")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], 12.32)
        self.assertEqual(data.hldata[-1][1], "y")
        self.assertEqual(data.num_radionuclides, 1252)
        self.assertEqual(data.radionuclides[0], "Fm-257")
        self.assertEqual(data.radionuclides[-1], "H-3")
        self.assertEqual(data.radionuclide_dict["Fm-257"], 0)
        self.assertEqual(data.radionuclide_dict["H-3"], 1251)
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[0], "Cf-253")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][0], 0.9979)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[0][1], "\u03b1")
        self.assertEqual(list(data.prog_bfs_modes[0].keys())[1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][0], 0.0021)
        self.assertEqual(list(data.prog_bfs_modes[0].values())[1][1], "SF")
        self.assertEqual(list(data.prog_bfs_modes[-1].keys())[0], "He-3")
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][0], 1.0)
        self.assertEqual(list(data.prog_bfs_modes[-1].values())[0][1], "\u03b2-")
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.scipy_data.year_conv, 365.2422)
        self.assertEqual(
            data.sympy_data.decay_consts[0],
            log(2) * Integer(10) / (Integer(1005) * Integer(24) * Integer(3600)),
        )
        self.assertEqual(data.sympy_data.ln2, log(2))
        self.assertEqual(data.sympy_data.matrix_c[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_c_inv[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_e[0, 0], Integer(0))
        self.assertEqual(data.sympy_data.vector_n0[0], Integer(0))
        self.assertEqual(data.sympy_data.year_conv, Integer(3652422) / Integer(10000))

    def test_decaydata_half_life(self):
        """
        Test DecayData half_life() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.half_life("H-3"), 388781329.30560005)
        self.assertEqual(data.half_life("H-3", "y"), 12.32)
        self.assertEqual(data.half_life("Fm-257", "h"), 2412.0)
        self.assertEqual(data.half_life("Rn-222", "d"), 3.8235)

        self.assertEqual(data.half_life("H-3", "readable"), "12.32 y")
        self.assertEqual(data.half_life("Po-213", "readable"), "4.2 μs")
        self.assertEqual(data.half_life("Ra-219", "readable"), "10 ms")
        self.assertEqual(data.half_life("Rn-215", "readable"), "2.30 μs")
        self.assertEqual(data.half_life("U-238", "readable"), "4.468 By")

    def test_decaydata_branching_fraction(self):
        """
        Test DecayData branching_fraction() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.branching_fraction("K-40", "Ca-40"), 0.8914)
        self.assertEqual(data.branching_fraction("K-40", "H-3"), 0.0)

    def test_decaydata_decay_mode(self):
        """
        Test DecayData decay_mode() method.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(data.decay_mode("K-40", "Ca-40"), "\u03b2-")
        self.assertEqual(data.decay_mode("K-40", "H-3"), "")

    def test_decaydata___eq__(self):
        """
        Test DecayData equality.
        """

        data1 = decaydata.DecayData("icrp107")
        data2 = decaydata.DecayData("icrp107")
        self.assertEqual(data1, data2)

    def test_decaydata___ne__(self):
        """
        Test DecayData not equality.
        """

        data1 = decaydata.DecayData("icrp107")
        data2 = decaydata.DecayData("icrp107")
        data2.dataset = "icrp07"
        self.assertNotEqual(data1, data2)

    def test_decaydata___repr__(self):
        """
        Test DecayData representations.
        """

        data = decaydata.DecayData("icrp107")
        self.assertEqual(
            data.__repr__(), "Decay dataset: icrp107, contains SymPy data: False"
        )

        data = decaydata.DecayData("icrp107", load_sympy=True)
        self.assertEqual(
            data.__repr__(), "Decay dataset: icrp107, contains SymPy data: True"
        )


if __name__ == "__main__":
    unittest.main()
