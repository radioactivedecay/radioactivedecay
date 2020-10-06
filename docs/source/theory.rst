Theory
======

Solution to decay chain differential equations
----------------------------------------------

``radioactivedecay`` implements the analytical solution to the decay chain
differential equations outlined by Amaku et al. :ref:`[1] <refs>`.

Consider a system of :math:`n` radionuclides, where the vector
:math:`\mathbf{N}(t)` has elements :math:`N_{i}(t)` representing the number
of atoms of radionuclide :math:`i` at time :math:`t`. The radioactive decay
chain differential equations can be expressed using matrix notation as

.. math::

    \frac{\mathrm{d}\mathbf{N}}{\mathrm{d}t} = \varLambda \mathbf{N}.
   
:math:`\varLambda` is a lower triangular matrix whose elements are

.. math::
    \varLambda_{ij} =
    \begin{cases}
    0 && \text{for }  i < j,\\
    -\lambda_{j} && \text{for }  i = j,\\
    b_{ji}\lambda_{j} && \text{for }  i > j.
    \end{cases}

where :math:`\lambda_{j}` is the decay constant of radionuclide :math:`j`,
and :math:`b_{ji}` is the branching fraction from radionuclide :math:`j` to 
:math:`i`.

The analytical solution to the differential equation can be expressed as

.. math::
    \mathbf{N}(t) = C E C^{-1} \mathbf{N}(0),

where :math:`E` is a diagonal matrix with elements
:math:`E_{ii} = e^{-\lambda_i t}`. :math:`C` is a lower triangular matrix with
elements

.. math::
    C_{ij} =
    \begin{cases}
    0 && \text{for }  i < j,\\
    1 && \text{for }  i = j,\\
    \frac{\sum_{k=j}^{i-1}\varLambda_{ik}C_{kj}}{\varLambda_{jj} - \varLambda_{ii}} && \text{for }  i > j,
    \end{cases}

and :math:`C^{-1}` is the inverse of :math:`C` that can be calculated as

.. math::
    C^{-1}_{ij} =
    \begin{cases}
    0 && \text{for }  i < j,\\
    1 && \text{for }  i = j,\\
    -\sum_{k=j}^{i-1} C_{ik} C^{-1}_{kj} && \text{for }  i > j.
    \end{cases}
    
Implementation in radioactivedecay
----------------------------------

As matrices :math:`C` and :math:`C^{-1}` are independent of time, they can be
pre-calculated and imported into ``radioactivedecay`` as part of a radioactive
decay dataset. They are pre-calculated for the ICRP-107 dataset
:ref:`[2] <refs>` in this
`Jupter notebook <https://github.com/alexmalins/radioactivedecay/notebooks/icrp107_dataset/icrp107_dataset.ipynb>`_
held in the package GitHub repository.

Note that :math:`C`, :math:`C^{-1}` and :math:`E` are sparse matrices. Storing
the matrices in sparse format greatly reduces the amount of memory that they
occupy and the computational time for the matrix multiplications. These
matrices are therefore stored in SciPy Compressed Sparse Column (CSC) matrix
format in ``radioactivedecay``.

References
----------

1. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
2. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_