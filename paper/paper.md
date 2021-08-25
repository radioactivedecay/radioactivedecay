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
  - name: Thom Lemoine
    affiliation: 2
affiliations:
- name: Center for Computational Science &amp; e-Systems (CCSE), Japan Atomic Energy Agency (JAEA), 178-4-4 Wakashiba, Kashiwa, Chiba, 277-0871, Japan
  index: 1
- name: Whitman College
  index: 2
date: XX April 2021
bibliography: paper.bib
---


# Summary

`radioactivedecay` is a Python package for radioactive decay modelling.
It contains functions to fetch decay data, define inventories of radionuclides and perform decay calculations.
The default nuclear decay dataset supplied with `radioactivedecay` is based on ICRP Publication 107, which covers 1252 radioisotopes of 97 elements.
The code calculates an analytical solution to a matrix form of the decay chain differential equations using double or higher precision numerical operations.
There are visualization functions for drawing decay chain diagrams and plotting activity decay curves.


# Statement of Need

Calculations for the decay of radioactivity and the ingrowth of progeny underpin the use of radioisotopes in a wide range of research and industrial fields, spanning from nuclear engineering, medical physics, radiation protection, environmental science and archaeology to non-destructive testing, mineral prospecting, food preservation, homeland security and defence.
`radioactivedecay` is an open source, cross-platform package for decay calculations and visualization.
It supports decay chains with branching decays and metastable nuclear isomers.
It includes a high numerical precision decay calculation mode which resolves numerical issues when using double-precision floating-point numbers for decaying chains containing radionuclides with disparate half-lives [@Bakin2018].

This set of features distinguishes `radioactivedecay` from other commonly-used decay packages, such as `Radiological Toolbox` and `PyNE`.
`Radiological Toolbox` is a closed-source Windows application, so it is not easily scriptable and its use of double-precision arithmetic makes it susceptible to numerical round-off errors.
`PyNE` uses approximations to help mitigate numerical issues, however these may potentially affect accuracy.
Moreover as of `v0.7.3`, `PyNE` does not correctly model metastable nuclear isomers within decay chains, which means, for example, it cannot simulate the production of $^{99m}\textrm{Tc}$ from $^{99}\textrm{Mo}$ for medical imaging applications.


# Theory and Implementation

`radioactivedecay` implements the solution to the decay differential equations outlined by @Amaku2010.
If vector $\mathbf{N}$ contains the number of atoms of each radionuclide in a system, its elements $N_i$ can be ordered such that no progeny (either first or subsequent generation) of radionuclide $i$ has itself an index lower than $i$.
Ordering in this manner is possible because natural radioactive decay processes do not increase the mass number of the decaying radionuclide, and there are no cyclic decay chains where radionuclide $i$ can decay to other radionuclides then reform itself [@Ladshaw2020].
Note metastable nuclear isomers have distinct indices from their ground states in $\mathbf{N}$.

The radioactive decay chain differential equations expressed in matrix form are:

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
b_{ji}\lambda_{j} & \textrm{for }  i > j.
\end{cases}
\end{equation}

$\lambda_{j}$ is the decay constant of radionuclide $j$, and $b_{ji}$ is the branching fraction from radionuclide $j$ to $i$.
$\varLambda$ is diagonalizable so its eigendecomposition can be used to rewrite \autoref{eq:diff_eq} as:

\begin{equation}
\frac{\mathrm{d}\mathbf{N}}{\mathrm{d}t} = C \varLambda_d C^{-1} \mathbf{N}.
\label{eq:diff_eq_rewrite}
\end{equation}

$\varLambda_d$ is a diagonal matrix whose elements are the negative decay constants, i.e. $\varLambda_{dii} = -\lambda_{i}$.
Matrix $C$ and its inverse $C^{-1}$ are both lower triangular matrices that are calculated as:

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

The analytical solution to \autoref{eq:diff_eq_rewrite} given an initial condition of $\mathbf{N}(0)$ at $t=0$ is:

\begin{equation}
\mathbf{N}(t) = C e^{\varLambda_{d} t} C^{-1} \mathbf{N}(0).
\label{eq:solution}
\end{equation}

$e^{\varLambda_{d} t}$ is a diagonal matrix with elements $e^{\varLambda_{d} t}_{ii} = e^{-\lambda_i t}$.
`radioactivedecay` evaluates \autoref{eq:solution} upon each call for a decay calculation.

Matrices $C$ and $C^{-1}$ are independent of time so they are pre-calculated and imported from files into `radioactivedecay`.
$C$ and $C^{-1}$ are stored in sparse matrix data structures to minimize memory use and maximize efficiency when computing the matrix multiplications in \autoref{eq:solution}.
For decay calculations with double-precision floating-point operations, $C$ and $C^{-1}$ are stored in `SciPy` [@Virtanen2020] Compressed Sparse Row (CSR) matrix data structures. 
Conversely, they are stored in `SymPy` [@Meurer2017] SparseMatrix data structures for high numerical precision calculations.

The high numerical precision decay calculation mode resolves numerical issues arising from using double-precision floating-point numbers for decay calculations for chains containing nuclides with disparate half-lives. 
One example is the decay chain for $^{254}\textrm{Es}$, which contains $^{238}\textrm{U}$ (4.468 billion year half-life) and $^{214}\textrm{Po}$ ($t_{1/2}$ is 164.3 $\mu$s half-life).
This a 20 orders of magnitude difference in half-life. 
Loss of numerical precision inevitably occurs when evaluating the off-diagonal elements of $C$ and $C^{-1}$ in \autoref{eq:c} with double-precision floating-point numbers (which hold approximately 15 decimal places of numerical precision).
Note loss of precision also occurs in the converse scenario, i.e. when a decay chain contains radionuclides with similar half-lives.
However this scenario does not occur in the ICRP Publication 107 decay dataset, as the relative difference between half-lives of any two radionuclides in the same decay chain is always greater than 0.1%.

The default operation of the high precision decay mode is to evaluate \autoref{eq:solution} using floating-point numbers with 320 significant figures of precision.
This is sufficient precision to ensure accurate results for any physically relevant decay calculation users may wish to perform.
Moreover, computations in the high precision mode are fast, taking only 0.5 seconds on a notebook equipped with an Intel Core i5-8250U processor.


# Decay Datasets

The default decay dataset supplied with `radioactivedecay` is based on ICRP Publication 107 [@ICRP107].
@Endo2005 and @Endo2007 describe the development of the ICRP Publication 107 decay dataset.
The raw data was converted into dataset files suitable for `radioactivedecay` using a Jupyter [notebook](https://github.com/alexmalins/radioactivedecay/tree/main/notebooks/icrp107_dataset/icrp107_dataset.ipynb). 
Along with `SciPy` and `SymPy` versions of the sparse matrices $C$ and $C^{-1}$, the dataset files store radionuclide half-lives, decay constants, progeny, branching fractions and decay modes.
Although ICRP Publication 107 is the default dataset, `radioactivedecay` allows users to import and use other decay datasets.


# Main Functionality

![Examples of the plotting capabilities of `radioactivedecay`: (a) Decay chain diagram for molybdenum-99. (b) Graph showing the decay of 1 kBq of $^{99}\textrm{Mo}$ along with the ingrowth of $^{99m}\textrm{Tc}$ and a trace quantity of $^{99}\textrm{Tc}$.\label{fig:decay_diags}](Mo-99.pdf)

The main functionality of `radioactivedecay` is based around two classes: the `Radionuclide` class and the `Inventory` class.
The `Radionuclide` class is used for fetching decay data about a single radionuclide, such as its half-life, the decay modes, the progeny and the branching fractions.
It creates diagrams of the radionuclide's decay chain (ex. \autoref{fig:decay_diags}(a)) based on `NetworkX` [@Hagberg2008].

An `Inventory` can contain multiple radionuclides, each with an associated radioactivity.
The `decay()` and `decay_high_precision()` methods calculate the decay of the `Inventory`, adding any ingrown radioactive progeny automatically.
Plots can be made of the variation of radionuclide activities over time (ex. \autoref{fig:decay_diags}(b)) based on `Matplotlib` [@Hunter2007].


# Validation

Decay calculations with `radioactivedecay v0.3.2` were cross-checked against `Radiological Toolbox v3.0.0` [@Hertel2015] and `PyNE v0.7.3` [@Scopatz2012] (see Jupyter [notebooks](https://github.com/alexmalins/radioactivedecay/notebooks/comparisons) in the project repository).
`Radiological Toolbox` employs the ICRP Publication 107 decay data.
Fifty radionuclides were randomly selected and a decay calculation was performed for 1 Bq of each for a random decay time within a factor of $10^{-3}$ to $10^{3}$ of the half-life.
Differences between decayed activities reported by each code were within 1% of each other in 64% of cases.
Discrepancies greater than 1% were attributed to rounding differences, erroneous results from `Radiological Toolbox`, or numerical issues relating to decay chains containing radionuclides with disparate half-lives.

A dataset was prepared for `radioactivedecay` with the same Evaluated Nuclear Structure Data File [@ENSDF] decay data as used by `PyNE v0.7.3`.
Bugs in `PyNE v0.7.3` cause incorrect decay calculation results for chains containing metastable nuclear isomers, $^{183}\textrm{Pt}$, $^{172}\textrm{Ir}$ or $^{152}\textrm{Lu}$.
Radionuclides affected by this were excluded from the comparison.
The decay of 1 Bq of every radionuclide was calculated for multiple decay times varying from 0 to $10^{6}$ times the radionuclide's half-life.
The absolute difference between the decayed activities reported by each code was less than $10^{-13}$ Bq.
Relative differences depended on the magnitude of the activity.
Relative errors of greater than 0.1% only occurred when the calculated activity was less than $2.5\times10^{-11}$ Bq, i.e. 10 orders of magnitude smaller than the initial activity of the parent radionuclide.
The discrepancies between the two codes were attributed to methodological differences for computing decay chains with radionuclides with large disparities between half-lives, and numerical issues arising from double-precision floating-point operations.


# Limitations

`radioactivedecay` does not model neutronics, so cannot evaluate radioactivity produced from activations or induced fission. It does not support external sources of radioactivity input or removal from an inventory over time. Caution is required if decaying backwards in time, as this can cause floating-point overflows when computing the exponential terms in \autoref{eq:solution}.

There are also some limitations associated with the ICRP Publication 107 decay dataset. It does not contain data for the radioactivity produced from spontaneous fission decay pathways and the minor decay pathways of some radionuclides. More details on limitations are available in the [documentation](https://alexmalins.com/radioactivedecay/overview.html#limitations), @Endo2005, and @Endo2007.


# Acknowledgements

We thank Mitsuhiro Itakura, Kazuyuki Sakuma &amp; colleagues in JAEA's Center for Computational Science &amp; Systems for their support for this project, Kenny McKee &amp; Daniel Jewell for helpful suggestions, and Bj&ouml;rn Dahlgren, Anthony Scopatz &amp; Jonathan Morrell for their work on radioactive decay calculation software.


# References
