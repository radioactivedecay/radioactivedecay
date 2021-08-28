"""
Unit tests for plots.py functions.
"""

import unittest
import matplotlib
import matplotlib.pyplot as plt
from radioactivedecay.plots import (
    _parse_nuclide_label,
    _parse_decay_mode_label,
    _check_fig_axes,
)


class TestPlotsFunctions(unittest.TestCase):
    """
    Unit tests for plots.py functions.
    """

    def test__parse_nuclide_label(self) -> None:
        """
        Test the parsing of nuclide strings for node labels.
        """

        self.assertEqual(_parse_nuclide_label("H-3"), "³H")
        self.assertEqual(_parse_nuclide_label("Be-7"), "⁷Be")
        self.assertEqual(_parse_nuclide_label("C-10"), "¹⁰C")
        self.assertEqual(_parse_nuclide_label("Ne-19"), "¹⁹Ne")
        self.assertEqual(_parse_nuclide_label("I-118"), "¹¹⁸I")
        self.assertEqual(_parse_nuclide_label("Pd-100"), "¹⁰⁰Pd")
        self.assertEqual(_parse_nuclide_label("Cl-34m"), "³⁴ᵐCl")
        self.assertEqual(_parse_nuclide_label("I-118m"), "¹¹⁸ᵐI")
        self.assertEqual(_parse_nuclide_label("Tb-156m"), "¹⁵⁶ᵐTb")
        self.assertEqual(_parse_nuclide_label("Tb-156n"), "¹⁵⁶ⁿTb")
        self.assertEqual(_parse_nuclide_label("SF"), "various")

    def test__parse_decay_mode_label(self) -> None:
        """
        Test the parsing of decay mode strings for edge labels.
        """

        self.assertEqual(_parse_decay_mode_label("α"), "α")
        self.assertEqual(_parse_decay_mode_label("β+"), "β⁺")
        self.assertEqual(_parse_decay_mode_label("β+ & EC"), "β⁺ & EC")
        self.assertEqual(_parse_decay_mode_label("β-"), "β⁻")
        self.assertEqual(_parse_decay_mode_label("EC"), "EC")
        self.assertEqual(_parse_decay_mode_label("IT"), "IT")
        self.assertEqual(_parse_decay_mode_label("SF"), "SF")

    def test__check_fig_axes(self) -> None:
        """
        Test the parsing of user-defined Matplotlib Figure and Axes objects.
        """

        fig_in, axes_in = plt.subplots()
        fig, axes = _check_fig_axes(fig_in, axes_in)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(axes, matplotlib.axes.Axes)

        fig, axes = _check_fig_axes(fig_in, None)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(axes, matplotlib.axes.Axes)

        fig, axes = _check_fig_axes(None, axes_in)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(axes, matplotlib.axes.Axes)

        fig, axes = _check_fig_axes(None, None)
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertIsInstance(axes, matplotlib.axes.Axes)


if __name__ == "__main__":
    unittest.main()
