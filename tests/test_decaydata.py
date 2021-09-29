"""
Unit tests for decaydata.py functions, classes and methods.
"""

import unittest
import numpy as np
from scipy import sparse
from sympy import Integer, log, Matrix
from sympy.matrices import SparseMatrix
from radioactivedecay import decaydata, icrp107_ame2020_nubase2020


class TestDecayDataFunctions(unittest.TestCase):
    """
    Unit tests for the decaydata.py functions.
    """

    # pylint: disable=protected-access

    def test__csr_matrix_equal(self) -> None:
        """
        Test function to check equality of two SciPy Compressed Sparse Row (CSR) matrices.
        """

        matrix_a = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_b = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c = sparse.csr_matrix(([1.0], ([1], [0])), shape=(2, 2))
        self.assertEqual(decaydata._csr_matrix_equal(matrix_a, matrix_b), True)
        self.assertEqual(decaydata._csr_matrix_equal(matrix_a, matrix_c), False)


class TestDecayMatrices(unittest.TestCase):
    """
    Unit tests for the decaydata.py DecayMatrices class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of DecayMatrices objects.
        """

        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([1], [1])), shape=(2, 2))
        decay_mats = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(decay_mats.atomic_masses[0], 0.0)
        self.assertEqual(decay_mats.atomic_masses[1], 0.0)
        self.assertEqual(decay_mats.decay_consts[0], 0.0)
        self.assertEqual(decay_mats.decay_consts[1], 0.0)
        self.assertEqual(decay_mats.ln2, np.log(2))
        self.assertEqual(decay_mats.matrix_c[0, 0], 1.0)
        self.assertEqual(decay_mats.matrix_c_inv[1, 1], 1.0)
        self.assertEqual(decay_mats.matrix_e[0, 0], 0.0)
        self.assertEqual(decay_mats.matrix_e[1, 1], 0.0)
        self.assertEqual(decay_mats.vector_n0[0], 0.0)
        self.assertEqual(decay_mats.vector_n0[1], 0.0)

    def test_decaymatrices___eq__(self) -> None:
        """
        Test DecayMatrices equality.
        """

        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        decay_mats_a = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        decay_mats_b = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(decay_mats_a, decay_mats_b)

        self.assertFalse(decay_mats_a == "random object")

    def test_decaymatrices___ne__(self) -> None:
        """
        Test DecayMatrices inequal.
        """

        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        decay_mats_a = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([2.0], ([0], [0])), shape=(2, 2))
        decay_mats_b = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertNotEqual(decay_mats_a, decay_mats_b)

        self.assertTrue(decay_mats_a != "random object")

    def test_decaymatrices___repr__(self) -> None:
        """
        Test DecayMatrices __repr__ strings.
        """

        atomic_masses = np.array([0.0] * 2)
        decay_consts = np.array([0.0] * 2)
        matrix_c = sparse.csr_matrix(([1.0], ([0], [0])), shape=(2, 2))
        matrix_c_inv = sparse.csr_matrix(([1.0], ([1], [1])), shape=(2, 2))
        decay_mats = decaydata.DecayMatrices(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(
            decay_mats.__repr__(),
            "DecayMatrices: data stored in SciPy/NumPy objects for double precision calculations.",
        )


class TestDecayMatricesSymPy(unittest.TestCase):
    """
    Unit tests for the decaydata.py DecayMatricesSympy class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of DecayMatricesSympy objects.
        """

        atomic_masses = Matrix.zeros(2, 1)
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        decay_mats = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(decay_mats.atomic_masses[0], 0.0)
        self.assertEqual(decay_mats.atomic_masses[1], 0.0)
        self.assertEqual(decay_mats.decay_consts[0], 0.0)
        self.assertEqual(decay_mats.decay_consts[1], 0.0)
        self.assertEqual(decay_mats.ln2, log(2))
        self.assertEqual(decay_mats.matrix_c[0, 0], Integer(2))
        self.assertEqual(decay_mats.matrix_c_inv[1, 1], Integer(3))
        self.assertEqual(decay_mats.matrix_e[0, 0], Integer(0))
        self.assertEqual(decay_mats.matrix_e[1, 1], Integer(0))
        self.assertEqual(decay_mats.vector_n0[0], 0.0)
        self.assertEqual(decay_mats.vector_n0[1], 0.0)

    def test___eq__(self) -> None:
        """
        Test DecayMatricesSympy equality.
        """

        atomic_masses = Matrix.zeros(2, 1)
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        decay_mats_a = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        atomic_masses = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        decay_mats_b = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(decay_mats_a, decay_mats_b)

        self.assertFalse(decay_mats_a == "random object")

    def test___ne__(self) -> None:
        """
        Test DecayMatricesSympy inequality.
        """

        atomic_masses = Matrix.zeros(2, 1)
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        decay_mats_a = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        atomic_masses = Matrix.zeros(2, 1)
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(5)
        decay_mats_b = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertNotEqual(decay_mats_a, decay_mats_b)

        self.assertTrue(decay_mats_a != "random object")

    def test___repr__(self) -> None:
        """
        Test DecayMatricesSympy __repr__ strings.
        """

        atomic_masses = Matrix.zeros(2, 1)
        decay_consts = Matrix.zeros(2, 1)
        matrix_c = SparseMatrix.zeros(2, 2)
        matrix_c[0, 0] = Integer(2)
        matrix_c_inv = SparseMatrix.zeros(2, 2)
        matrix_c_inv[1, 1] = Integer(3)
        decay_mats = decaydata.DecayMatricesSympy(
            atomic_masses, decay_consts, matrix_c, matrix_c_inv
        )
        self.assertEqual(
            decay_mats.__repr__(),
            "DecayMatricesSympy: data stored in SymPy objects for arbitrary-precision "
            + "calculations.",
        )


class TestDecayData(unittest.TestCase):
    """
    Unit tests for the decaydata.py DecayData class.
    """

    def test_instantiation(self) -> None:
        """
        Test instantiation of DecayData objects.
        """

        # pylint: disable=too-many-statements

        # check instantiation from sub-package
        data = decaydata.DecayData("icrp107_ame2020_nubase2020", load_sympy=False)
        self.assertEqual(data.dataset_name, "icrp107_ame2020_nubase2020")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], np.inf)
        self.assertEqual(data.hldata[-1][1], "s")
        self.assertEqual(data.nuclides[0], "Fm-257")
        self.assertEqual(data.nuclides[-1], "He-3")
        self.assertEqual(data.nuclide_dict["Fm-257"], 0)
        self.assertEqual(data.nuclide_dict["He-3"], 1497)
        self.assertEqual(data.progeny[0][0], "Cf-253")
        self.assertEqual(data.bfs[0][0], 0.9979)
        self.assertEqual(data.modes[0][0], "\u03b1")
        self.assertEqual(data.progeny[0][1], "SF")
        self.assertEqual(data.bfs[0][1], 0.0021)
        self.assertEqual(data.modes[0][1], "SF")
        self.assertEqual(data.progeny[-1], [])
        self.assertEqual(data.bfs[-1], [])
        self.assertEqual(data.modes[-1], [])
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.sympy_data, None)

        # check instantiation with supplied dataset path
        data = decaydata.DecayData(
            "icrp107_ame2020_nubase2020_2",
            icrp107_ame2020_nubase2020.__path__[0],
            load_sympy=False,
        )
        self.assertEqual(data.dataset_name, "icrp107_ame2020_nubase2020_2")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], np.inf)
        self.assertEqual(data.hldata[-1][1], "s")
        self.assertEqual(data.nuclides[0], "Fm-257")
        self.assertEqual(data.nuclides[-1], "He-3")
        self.assertEqual(data.nuclide_dict["Fm-257"], 0)
        self.assertEqual(data.nuclide_dict["He-3"], 1497)
        self.assertEqual(data.progeny[0][0], "Cf-253")
        self.assertEqual(data.bfs[0][0], 0.9979)
        self.assertEqual(data.modes[0][0], "\u03b1")
        self.assertEqual(data.progeny[0][1], "SF")
        self.assertEqual(data.bfs[0][1], 0.0021)
        self.assertEqual(data.modes[0][1], "SF")
        self.assertEqual(data.progeny[-1], [])
        self.assertEqual(data.bfs[-1], [])
        self.assertEqual(data.modes[-1], [])
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(data.sympy_data, None)

        # check instantiation from sub-package with SymPy data
        data = decaydata.DecayData("icrp107_ame2020_nubase2020", load_sympy=True)
        self.assertEqual(data.dataset_name, "icrp107_ame2020_nubase2020")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], np.inf)
        self.assertEqual(data.hldata[-1][1], "s")
        self.assertEqual(data.nuclides[0], "Fm-257")
        self.assertEqual(data.nuclides[-1], "He-3")
        self.assertEqual(data.nuclide_dict["Fm-257"], 0)
        self.assertEqual(data.nuclide_dict["He-3"], 1497)
        self.assertEqual(data.progeny[0][0], "Cf-253")
        self.assertEqual(data.bfs[0][0], 0.9979)
        self.assertEqual(data.modes[0][0], "\u03b1")
        self.assertEqual(data.progeny[0][1], "SF")
        self.assertEqual(data.bfs[0][1], 0.0021)
        self.assertEqual(data.modes[0][1], "SF")
        self.assertEqual(data.progeny[-1], [])
        self.assertEqual(data.bfs[-1], [])
        self.assertEqual(data.modes[-1], [])
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(
            data.sympy_data.decay_consts[0],
            log(2) * Integer(10) / (Integer(1005) * Integer(24) * Integer(3600)),
        )
        self.assertEqual(data.sympy_data.ln2, log(2))
        self.assertEqual(data.sympy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_c[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_c_inv[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_e[0, 0], Integer(0))
        self.assertEqual(data.sympy_data.vector_n0[0], Integer(0))

        # check instantiation with supplied dataset path with SymPy data
        data = decaydata.DecayData(
            "icrp107_ame2020_nubase2020_2",
            icrp107_ame2020_nubase2020.__path__[0],
            load_sympy=True,
        )
        self.assertEqual(data.dataset_name, "icrp107_ame2020_nubase2020_2")
        self.assertEqual(data.hldata[0][0], 100.5)
        self.assertEqual(data.hldata[0][1], "d")
        self.assertEqual(data.hldata[-1][0], np.inf)
        self.assertEqual(data.hldata[-1][1], "s")
        self.assertEqual(data.nuclides[0], "Fm-257")
        self.assertEqual(data.nuclides[-1], "He-3")
        self.assertEqual(data.nuclide_dict["Fm-257"], 0)
        self.assertEqual(data.nuclide_dict["He-3"], 1497)
        self.assertEqual(data.progeny[0][0], "Cf-253")
        self.assertEqual(data.bfs[0][0], 0.9979)
        self.assertEqual(data.modes[0][0], "\u03b1")
        self.assertEqual(data.progeny[0][1], "SF")
        self.assertEqual(data.bfs[0][1], 0.0021)
        self.assertEqual(data.modes[0][1], "SF")
        self.assertEqual(data.progeny[-1], [])
        self.assertEqual(data.bfs[-1], [])
        self.assertEqual(data.modes[-1], [])
        self.assertEqual(
            data.scipy_data.decay_consts[0], np.log(2) / (100.5 * 24 * 60 * 60)
        )
        self.assertEqual(data.scipy_data.ln2, np.log(2))
        self.assertEqual(data.scipy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_c_inv[0, 0], 1.0)
        self.assertEqual(data.scipy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.scipy_data.matrix_e[0, 0], 0.0)
        self.assertEqual(data.scipy_data.vector_n0[0], 0.0)
        self.assertEqual(
            data.sympy_data.decay_consts[0],
            log(2) * Integer(10) / (Integer(1005) * Integer(24) * Integer(3600)),
        )
        self.assertEqual(data.sympy_data.ln2, log(2))
        self.assertEqual(data.sympy_data.matrix_c.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_c[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_c_inv.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_c_inv[0, 0], Integer(1))
        self.assertEqual(data.sympy_data.matrix_e.shape, (1498, 1498))
        self.assertEqual(data.sympy_data.matrix_e[0, 0], Integer(0))
        self.assertEqual(data.sympy_data.vector_n0[0], Integer(0))

    def test_half_life(self) -> None:
        """
        Test DecayData half_life() method.
        """

        data = decaydata.DecayData("icrp107_ame2020_nubase2020")
        self.assertEqual(data.half_life("H-3"), 388781329.30560005)
        self.assertEqual(data.half_life("H-3", "y"), 12.32)
        self.assertEqual(data.half_life("Fm-257", "h"), 2412.0)
        self.assertEqual(data.half_life("Rn-222", "d"), 3.8235)

        self.assertEqual(data.half_life("H-3", "readable"), "12.32 y")
        self.assertEqual(data.half_life("Po-213", "readable"), "4.2 μs")
        self.assertEqual(data.half_life("Ra-219", "readable"), "10 ms")
        self.assertEqual(data.half_life("Rn-215", "readable"), "2.30 μs")
        self.assertEqual(data.half_life("U-238", "readable"), "4.468 By")

    def test_branching_fraction(self) -> None:
        """
        Test DecayData branching_fraction() method.
        """

        data = decaydata.DecayData("icrp107_ame2020_nubase2020")
        self.assertEqual(data.branching_fraction("K-40", "Ca-40"), 0.8914)
        self.assertEqual(data.branching_fraction("K-40", "H-3"), 0.0)
        self.assertEqual(data.branching_fraction("Cu-64", "Ni-64"), 0.61)

    def test_decay_mode(self) -> None:
        """
        Test DecayData decay_mode() method.
        """

        data = decaydata.DecayData("icrp107_ame2020_nubase2020")
        self.assertEqual(data.decay_mode("K-40", "Ca-40"), "\u03b2-")
        self.assertEqual(data.decay_mode("K-40", "H-3"), "")
        self.assertEqual(data.decay_mode("Cu-64", "Ni-64"), "\u03b2+ & EC")

    def test_decaydata___eq__(self) -> None:
        """
        Test DecayData equality.
        """

        data1 = decaydata.DecayData("icrp107_ame2020_nubase2020")
        data2 = decaydata.DecayData("icrp107_ame2020_nubase2020")
        self.assertEqual(data1, data2)

        self.assertFalse(data1 == "random object")

    def test_decaydata___ne__(self) -> None:
        """
        Test DecayData inequality.
        """

        data1 = decaydata.DecayData("icrp107_ame2020_nubase2020")
        data2 = decaydata.DecayData("icrp107_ame2020_nubase2020")
        data2.dataset_name = "icrp07"
        self.assertNotEqual(data1, data2)

        self.assertTrue(data1 != "random object")

    def test_decaydata___repr__(self) -> None:
        """
        Test DecayData __repr__ strings.
        """

        data = decaydata.DecayData("icrp107_ame2020_nubase2020")
        self.assertEqual(
            data.__repr__(),
            "Decay dataset: icrp107_ame2020_nubase2020, contains SymPy data: False",
        )

        data = decaydata.DecayData("icrp107_ame2020_nubase2020", load_sympy=True)
        self.assertEqual(
            data.__repr__(),
            "Decay dataset: icrp107_ame2020_nubase2020, contains SymPy data: True",
        )


if __name__ == "__main__":
    unittest.main()
