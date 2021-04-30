---
title: "radioactivedecay: A Python package for radioactive decay calculations"
tags:
  - Python
  - radioactivity
  - decay
  - decay chains
  - radionuclides
  - radioisotopes
authors:
  - name: Alex Malins
    orcid: 0000-0003-1922-4496
    affiliation: 1
affiliations:
- name: Center for Computational Science &amp; e-Systems (CCSE), Japan Atomic Energy Agency (JAEA), 178-4-4 Wakashiba, Kashiwa, Chiba, 277-0871, Japan
  index: 1
date: XX April 2021
bibliography: paper.bib
---


# Summary

`radioactivedecay` is a Python package for modelling and visualizing the decay of radioactive nuclides.
It contains functions to fetch decay data, draw diagrams of decay chains, define inventories of radionuclides, perform radioactive decay calculations, and plot activity decay and ingrowth curves.
The default nuclear decay dataset supplied with `radioactivedecay` is based on ICRP Publication 107, which covers 1252 radioiostopes of 97 elements.
ICRP Publication 107 data is widely used in radiation protection science, however `radioactivedecay` also supports the import and use alternative decay datasets.

The package can calculate the decay of chains of radionuclides, including ones containing branching decays and metastable nuclear isomers.
It solves the decay chain differential equations analytically by evaluating one matrix exponential and three matrix multiplications.
`NumPy` and `SciPy` linear algebra routines are called for performing calculations with double-precision floating-point numbers.
An alternative high numerical precision decay calculation mode employs `SymPy` arbitrary precision linear algebra routines.
The high precision mode is useful for calculating the decay of chains of radionuclides with orders of magnitude different half-lives, as round-off errors can cause numerical issues when using normal floating-point arithmetic for such calculations.
The code includes visualization functions for plotting decay chain diagrams and activity graphs.
The visualization functions are based on the `NetworkX` and `Matplotlib` libraries.

`radioactivedecay` is open source software for Python v3.6+ released under the MIT License.
It is platform independent and has been tested on Windows 10 (20H2), macOS (10.13) and Linux Ubuntu (20.04).
The source code is hosted on [GitHub](https://github.com/alexmalins/radioactivedecay) and online documentation is available at [https://alexmalins.com/radioactivedecay](https://alexmalins.com/radioactivedecay).
The package can be installed from the Python Package Index ([PyPI](https://pypi.org/project/radioactivedecay/)) using the `pip` command: ``pip install radioactivedecay``.


# Statement of Need

Radioactivity features in a wide range of research fields and industrial applications, including nuclear engineering, medical physics, radiation protection, environmental sciences, non-destructive testing, mining, food preservation, homeland security, defence and archaeology.
Calculations for the decay of radioactivity and the ingrowth of progeny underpin the use of radionuclides in these fields.

`radioactivedecay` was developed as a free, open source, easy to install and use, cross-platform package for decay calculations and visualization.
The package is programmed in Python, which is a popular programming language for scientific data analysis and modelling.
It is supplied with a large radioactive decay dataset and the code is able to calculate the decay of chains incorporating branching decays and metastable nuclear isomers.
The code includes a high numerical precision decay mode, which solves floating-point numerical issues when calculating the decay of chains of radionuclides with disparate half-lives.


# Theory and Implementation

`radioactivedecay` calculates an analytical solution to a matrix form of the decay chain differential equations using the method outlined by @Amaku2010.
This section summarizes the theory and computational details for how `radioactivedecay` performs decay calculations.

For a decay dataset containing $n$ radionuclides, let vector $\mathbf{N}$ have elements $N_{i}$ representing the number of atoms of each radionuclide.
The radionuclides in $\mathbf{N}$ can be ordered such that no progeny (either first or any subsequent generation) of radionuclide $i$ has an index lower than $i$.
This is possible because natural radioactive decay processes do not increase the mass number of the decaying radionuclide, and there are no cyclic decay chains, i.e. chain where radionuclide $i$ can decay through other radionuclides then reform itself [@Ladshaw2020].
Note metastable nuclear isomers (e.g. $^{192\textrm{m}}\textrm{Ir}$ and $^{192\textrm{n}}\textrm{Ir}$) are considered as a distinct radionuclides from the ground state (i.e. from $^{192}\textrm{Ir}$).

The radioactive decay chain differential equations can be expressed in matrix form as:

\begin{equation}
\frac{\mathrm{d}\mathbf{N}}{\mathrm{d}t} = \varLambda \mathbf{N}.
\label{eq:diff_eq}
\end{equation}

$\varLambda$ is a lower triangular matrix with elements:

\begin{equation}
\varLambda_{ij} =
\begin{cases}
0 & \textrm{for }  i < j,\\
-\lambda_{j} & \textrm{for }  i = j,\\
b_{ji}\lambda_{j} & \textrm{for }  i > j,
\end{cases}
\end{equation}

where $\lambda_{j}$ is the decay constant of radionuclide $j$, and $b_{ji}$ is the branching fraction from radionuclide $j$ to $i$.
$\varLambda$ is a diagonalizable matrix and its eigendecomposition can be used to rewrite \autoref{eq:diff_eq} as:

\begin{equation}
\frac{\mathrm{d}\mathbf{N}}{\mathrm{d}t} = C \varLambda_d C^{-1} \mathbf{N}.
\label{eq:diff_eq_rewrite}
\end{equation}

$\varLambda_d$ is a diagonal matrix whose elements are the negative decay constants ($\varLambda_{dii} = -\lambda_{i}$), which are the eigenvalues of $\varLambda$.
Matrix $C$ and its inverse $C^{-1}$ are both lower triangular matrices.
The column vectors of $C$ are the eigenvectors of $\varLambda$.
@Amaku2010 showed that $C$ and $C^{-1}$ can be calculated by:

\begin{equation}
C_{ij} =
\begin{cases}
0 & \text{for }  i < j,\\
1 & \text{for }  i = j,\\
\frac{\sum_{k=j}^{i-1}\varLambda_{ik}C_{kj}}{\varLambda_{jj} - \varLambda_{ii}} & \text{for }  i > j,
\end{cases}
\quad\text{and}\quad 
C^{-1}_{ij} =
\begin{cases}
0 & \text{for }  i < j,\\
1 & \text{for }  i = j,\\
-\sum_{k=j}^{i-1} C_{ik} C^{-1}_{kj} & \text{for }  i > j.
\end{cases}
\label{eq:c}
\end{equation}

The analytical solution to \autoref{eq:diff_eq_rewrite}, given an initial condition of $\mathbf{N}(0)$ at $t=0$, is:

\begin{equation}
\mathbf{N}(t) = C e^{\varLambda_{d} t} C^{-1} \mathbf{N}(0).
\label{eq:solution}
\end{equation}

Here $e^{\varLambda_{d} t}$ is the matrix exponential of $\varLambda_{d} t$, which is easy to calculate because $\varLambda_{d}$ is diagonal.
$e^{\varLambda_{d} t}$ is also therefore a diagonal matrix, and its elements are $e^{\varLambda_{d} t}_{ii} = e^{-\lambda_i t}$.

`radioactivedecay` evaluates \autoref{eq:solution} upon each call for a decay calculation.
Matrices $C$ and $C^{-1}$ are independent of time, so they are pre-calculated and loaded into memory upon creation of a `DecayData` object, which is the data structure `radioactivedecay` uses to store decay data.
As $C$ and $C^{-1}$ are sparse matrices, they are stored in sparse matrix data structures for efficient memory use and computations when evaluating the matrix multiplications in \autoref{eq:solution}.
$C$ and $C^{-1}$ are stored in `SciPy` [@Virtanen2020] Compressed Sparse Row (CSR) sparse matrices for performing standard decay calculations with double-precision floating-point numbers, and `NumPy` [@Harris2020] `ndarray` data structures are used to store the radionuclide number ($\mathbf{N}$) and activity vectors.

One issue that may arise when using fixed precision floating-point numbers for decay calculations is the loss of numerical precision that may occur when calculating the decay of chains containing radionuclides with orders of magnitude different half-lives.
For example the decay chain for $^{254}\textrm{Es}$ contains both $^{238}\textrm{U}$ ($t_{1/2}$ is 4.468 billion years) and $^{214}\textrm{Po}$ ($t_{1/2}$ is 164.3 $\mu$s), which is a 20 orders of magnitude difference in half-life.
Subtracting the two decay constants when pre-calculating the off-diagonal elements of $C$ (\autoref{eq:c}) inevitably results in loss of numerical accuracy if using double-precision floating-point numbers, which have approximately 15 decimal places of numerical precision.
Loss of significance occurs in the converse scenario, i.e. when a decay chain contains radionuclides with nearly identical half-lives.
However this scenario does not occur for the radionuclides in the ICRP Publication 107 decay dataset, as the relative difference between the decay constants of any two radionuclides in the same decay chain is always greater than 0.1%.

`radioactivedecay` addresses the double-precision floating-point arithmetic issues by offering a high precision decay calculation mode based on `SymPy` [@Meurer2017] arbitrary precision computation routines.
The default operation of the mode is to evaluate \autoref{eq:solution} using numbers with 320 significant figures of numerical precision.
This is sufficiently many significant figures to give accurate calculation results for any physically relevant decay scenario a user may wish to evaluate.
Decay calculations using this mode are also reasonably fast, taking only 0.5 seconds on a laptop computer equiped with an Intel Core i5-8250U processor.
The calculation results are cast to double-precision floating-point numbers for return to users.
The `SymPy` versions of $C$ and $C^{-1}$ are stored in `SymPy`'s `SparseMatrix` format within `DecayData` objects.


# Decay Datasets

The default decay dataset supplied with `radioactivedecay` is based on ICRP Publication 107 [@ICRP107].
The dataset includes decay data for 1252 radioiostopes of 97 elements.
@Endo2005 and @Endo2007 describe the creation process of ICRP Publication 107.
The ICRP Publication 107 data was converted into dataset files readable by `radioactivedecay` using a Jupyter [notebook](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/icrp107_dataset/icrp107_dataset.ipynb). 
Along with `SciPy` and `SymPy` versions of the sparse matrices $C$ and $C^{-1}$, the dataset files include data for radionuclide half-lives, decay constants, progeny, branching fractions and decay modes.

Data read in from dataset files are stored in `DecayData` objects.
The default ICRP Publication 107 data is read from packaged dataset files into memory upon the Python `import` statement for `radioactivedecay`.
Once `radioactivedecay` has been imported, it is possible for users to load alternative decay datasets by instantiating further `DecayData` objects.


# Functionality

![Examples of the plotting capabilities of `radioactivedecay`: (a) Decay chain diagram for molybdenum-99. (b) Graph showing the decay of 1 kBq of $^{99}\textrm{Mo}$ along with the ingrowth of $^{99m}\textrm{Tc}$ and a trace quantity of $^{99}\textrm{Tc}$.\label{fig:decay_diags}](Mo-99.pdf)

The main functionality of `radioactivedecay` is based around two classes: the `Radionuclide` class and the `Inventory` class.
The `Radionuclide` class is used for fetching decay data about a single radionuclide, such as its half-life, the decay modes, the progeny and the branching fractions.
The `plot()` method is used for creating diagrams of the radionuclide's decay chain, e.g. \autoref{fig:decay_diags}(a).
These plots are created using the `NetworkX` library [@Hagberg2008].

The `Inventory` class is used for radioactive decay calculations.
An `Inventory` instance may contain multiple radionuclides, each with an associated radioactivity.
The `decay()` and `decay_high_precision()` methods are used for decay calculations.
Users do not have to specify a unit of radioactivity (e.g. Bq, Ci, dpm) to use these methods, as the activity units of the decayed `Inventory` are the same as those for the initial `Inventory`.
Radioactive progeny that are not present in the initial `Inventory` are added automatically to the decayed `Inventory`.
The `plot()` method can be used to graph the variation of radionuclide activities over time, e.g. \autoref{fig:decay_diags}(b).
The plots are created using `Matplotlib` [@Hunter2007].


# Validation

The results of decay calculations from `radioactivedecay v0.3.2` were cross-checked against those from `Radiological Toolbox v3.0.0` [@Hertel2015] and `PyNE v0.7.3` [@Scopatz2012].
The comparisons are shown in Jupyter [notebooks](https://github.com/alexmalins/radioactivedecay/notebooks/comparisons) held in the `radioactivedecay` `git` repository.

`Radiological Toolbox` uses the ICRP Publication 107 nuclear decay data for decay calculations, i.e. identical data to the default for `radioactivedecay`.
50 radionuclides were randomly selected from ICRP Publication 107, and a decay calculation was performed for 1 Bq of each for a randomly selected decay time within a factor of $10^{-3}$ to $10^{3}$ of the radionuclide's half-life.
The decayed activities reported by `radioactivedecay` and `Radiological Toolbox` were within 1% of each other in 64% of cases.
Discrepancies greater than 1% were attributed to either simple rounding differences between the reported results, errors in computations performed by `Radiological Toolbox`, or numerical issues arising from computations for decay chains that contain radionuclides with orders of magnitude disparities between the half-lives.

Decay calculations in `PyNE v0.7.3` are based on decay data from the Evaluated Nuclear Structure Data File (ENSDF) database [@ENSDF].
A dataset was prepared for `radioactivedecay` with identical decay data to `PyNE v0.7.3` to undertake a like-for-like comparison of decay calculation results between the two codes.
The dataset included all the ground state radionuclides in `PyNE v0.7.3` with finite half-life.
Metastable nuclear isomers were excluded as `PyNE v0.7.3` does not correctly model the decay of chains containing metastable states.
Furthermore, decay chains containing $^{183}\textrm{Pt}$, $^{172}\textrm{Ir}$ or $^{152}\textrm{Lu}$ were truncated at these radionuclides, as each of these radionuclides has a progeny which has an identical half-life ($^{179}\textrm{Os}$, $^{168}\textrm{Re}$ and $^{149}\textrm{Tm}$, respectively).
`radioactivedecay` cannot calculate decay chains containing radionuclides with degenerate half-lives, and `PyNE v0.7.3` has a bug which gives incorrect decay results for such chains.

A comparison was performed by setting 1 Bq of each radionuclide in turn, then calculating decayed activities for decay periods that were a factor of 0 to $10^{6}$ times the radionuclide's half-life.
The absolute difference between the decayed activity reported for any radionuclide by the two codes was always less than $10^{-13}$ Bq.
The relative difference between calculated activities depended on the magnitude of the activity.
Relative errors of greater than 0.1% occurred only when the calculated activity was less than $2.5\times10^{-11}$ Bq, i.e. 10 orders of magnitude lower than the original activity of the parent radionuclide.
The differences between the results of the two codes were attributed to the different ways they calculate decay chains containing radionuclides with large disparities between half-lives, and numerical issues relating to the use of double-precision floating-point arithmetic.  


# Limitations

`radioactivedecay` has the following physics and computation limitations:

* It does not model neutronics, so cannot calculate the activity of radionuclides produced from neutron-nuclear activations or induced fission.
* It cannot model temporal sources of external radioactivity input to or removal from an inventory.
* Care is needed when using `decay()` to decay backwards in time, as this can cause floating-point overflows on computation of the exponentials for \autoref{eq:solution}.

There are also some limitations with respect to the ICRP Publication 107 decay data:

* ICRP Publication 107 does not contain data for the radioactivity progeny produced from spontaneous fission decays.
* Decay data is quoted in ICRP Publication 107 with up to 5 significant figures of precision, thus the results of decay calculations using this dataset will never be more precise than this.
* Uncertainties are not quoted for the decay data in ICRP Publication 107. Uncertainties will vary substantially between radionuclides, depending on how well each radionuclide has been researched in the past. The uncertainties may be more significant for the results of some decay calculations than the previous point about the quoted precision of the data in ICRP Publication 107.
* There are some minor decay pathways that were not included in ICRP Publication 107. Examples include the decays $^{219}\textrm{At}\,\to\,^{219}\textrm{Rn}$ ($\beta^{\textrm{-}}$ decay, branching fraction ~3%), $^{250}\textrm{Es}\,\to\,^{246}\textrm{Bk}$ ($\alpha$ decay, ~1.5%), and $^{228}\textrm{U}\,\to\,^{228}\textrm{Pa}$ (electron capture decay, ~2.5%). For more details on these cases and others, see the references on the creation of the ICRP Publication 107 data [@Endo2005; @Endo2007].
* Radioactive progeny resulting from some decay pathways present in ICRP Publication 107 are not themselves included in the publication. The missing radionuclides all have extremely long half-lives and can be considered as practically stable, e.g. $^{184}\textrm{Os}$, which results from the decay of $^{184}\textrm{Ir}$, has a half-life of over 56,000 billion years. 


# Acknowledgements

We thank Mitsuhiro Itakura, Kazuyuki Sakuma &amp; colleagues in JAEA's Center for Computational Science &amp; Systems for their support for this project, Kenny McKee &amp; Daniel Jewell for helpful suggestions, and Bj&ouml;rn Dahlgren, Anthony Scopatz &amp; Jonathan Morrell for their work on radioactive decay calculation software.


# References
