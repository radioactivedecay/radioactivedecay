Theory
======

Solution to the decay chain differential equations
--------------------------------------------------

``radioactivedecay`` calculates an analytical solution to the decay chain
differential equations using the method outlined by Amaku et al. :ref:`[1]
<refs>`.

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

:math:`\varLambda` is a diagonalizable matrix so its eigendecomposition can be
used to rewrite the matrix differential equation as

.. math::

    \frac{\mathrm{d}\mathbf{N}}{\mathrm{d}t} = C \varLambda_d C^{-1} \mathbf{N}.

Here :math:`\varLambda_d` is a diagonal matrix whose elements along the
diagonal are the negative decay constants
(:math:`\varLambda_{dii} = -\lambda_{i}`, these are the eigenvalues of
:math:`\varLambda`). Matrix :math:`C` and its inverse :math:`C^{-1}` are both
lower triangular matrices. The column vectors of :math:`C` are the eigenvectors
of :math:`\varLambda`. Amaku et al. showed the elements of :math:`C` can be
calculated as

.. math::
    C_{ij} =
    \begin{cases}
    0 && \text{for }  i < j,\\
    1 && \text{for }  i = j,\\
    \frac{\sum_{k=j}^{i-1}\varLambda_{ik}C_{kj}}{\varLambda_{jj} - \varLambda_{ii}} && \text{for }  i > j.
    \end{cases}

The elements of the inverse matrix :math:`C^{-1}` can then be calculated as

.. math::
    C^{-1}_{ij} =
    \begin{cases}
    0 && \text{for }  i < j,\\
    1 && \text{for }  i = j,\\
    -\sum_{k=j}^{i-1} C_{ik} C^{-1}_{kj} && \text{for }  i > j.
    \end{cases}


The analytical solution to the matrix differential equation given the intial
condition :math:`\mathbf{N}(t=0)=\mathbf{N}(0)` is

.. math::
    \mathbf{N}(t) = C e^{\varLambda_{d} t} C^{-1} \mathbf{N}(0).

This is the equation that is calculated by ``radioactivedecay`` upon each call
to ``decay()``. :math:`e^{\varLambda_{d} t}` is the matrix exponential of
:math:`\varLambda_{d} t`. It is a diagonal matrix with elements
:math:`e^{\varLambda_{d} t}_{ii} = e^{-\lambda_i t}`. 

The final equation that is needed is the conversion between the activity
(:math:`\mathbf{A}`) and number of atoms (:math:`\mathbf{N}`) vectors.
:math:`\mathbf{A}` is just an element-wise multiplication of the decay constants
and the number of atoms:

.. math::
    A_i = \lambda_i N_i.
    
Implementation in radioactivedecay
----------------------------------

As matrices :math:`C` and :math:`C^{-1}` are independent of time, they can be
pre-calculated and imported into ``radioactivedecay`` as part of a radioactive
decay dataset.  :math:`C` and :math:`C^{-1}`  are pre-calculated for the
ICRP-107 :ref:`[2] <refs>` dataset in
`this Jupter notebook <https://github.com/alexmalins/radioactivedecay/notebooks/tree/main/icrp107_dataset/icrp107_dataset.ipynb>`_
held in the GitHub repository.

Note that :math:`C`, :math:`C^{-1}` and :math:`e^{\varLambda_{d} t}` are sparse
matrices. Storing the matrices in a sparse matrix format greatly reduces the
amount of memory that they occupy and the computational time for the matrix
multiplications in the ``decay()`` operation. The matrices are therefore stored
in SciPy Compressed Sparse Column (CSC) matrix format in ``radioactivedecay``.

References
----------

1. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
2. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_