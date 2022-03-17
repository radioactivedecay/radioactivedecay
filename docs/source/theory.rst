Theory and Computation
======================

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
    b_{ji}\lambda_{j} && \text{for }  i > j,
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

The final equations that are needed are for converting between various
quantities. Converting between mass (:math:`\mathbf{M}`, in grams) and
number of atoms (:math:`\mathbf{N}`) uses the vector of atomic masses
(:math:`\mathbf{M_u}`) and the Avogadro constant (:math:`N_a`):

.. math::
    M_i =  \frac{M_{ui} N_i}{N_a}.

Converting between activity (:math:`\mathbf{A}`) and number of atoms
(:math:`\mathbf{N}`) uses the vector of decay constants
(:math:`\mathbf{\lambda}`):

.. math::
    A_i = \lambda_i N_i.
    
Implementation in radioactivedecay
----------------------------------

As matrices :math:`C` and :math:`C^{-1}` are independent of time, they can be
pre-calculated and imported into ``radioactivedecay`` as part of a radioactive
decay dataset.  :math:`C` and :math:`C^{-1}`  are pre-calculated for the
ICRP-107 :ref:`[2] <refs>` dataset in
`this Jupyter notebook
<https://github.com/radioactivedecay/datasets/blob/main/icrp107_ame2020_nubase2020/icrp107_dataset.ipynb>`_.

Note that :math:`C`, :math:`C^{-1}` and :math:`e^{\varLambda_{d} t}` are sparse
matrices. Storing the matrices in a sparse matrix format greatly reduces the
amount of memory that they occupy and the computational expense for the matrix
multiplications in each decay calculation.

Notes on computation and numerical precision
--------------------------------------------

Numerical issues can arise when using double-precision floating-point numbers
to compute decays for some chains :ref:`[3] <refs>`. For example, the Es-254
decay chain contains U-238 (half-life 4.468 billion years) and Po-214
(half-life 164.3 microseconds), which is a 20 orders of magnitude difference in
half-life. Round-off errors and loss of significance can occur causing
unphysical results, e.g.

.. code-block:: python3

    >>> inv = rd.Inventory({'Es-254': 1.0})
    >>> inv.decay(0.0).activities()
    {'At-218': -8.24439035981494e-30, 'Bi-210': 2.5308844932098316e-26,
     'Bi-214': -4.256549745172888e-26, 'Bk-250': 0.0,
     'Cf-250': 0.0, 'Cm-246': 8.802967479989175e-21,
     'Es-254': 1.0, 'Fm-254': 0.0,
     'Hg-206': -3.4696439711117526e-34, 'Pa-234': 2.330729590281097e-29,
     'Pa-234m': -1.5696690930108473e-26, 'Pb-206': 0.0,
     'Pb-210': 2.673060958594837e-26, 'Pb-214': -7.310828272597407e-27,
     'Po-210': -1.048466176320909e-27, 'Po-214': 2.3260114484256133e-26,
     'Po-218': -1.1433437709020225e-26, 'Pu-242': 1.3827905917787723e-22,
     'Ra-226': -1.0811575068833228e-26, 'Rn-218': -1.618765025703667e-33,
     'Rn-222': -1.581593359682259e-26, 'Th-230': -1.2628442466252288e-26,
     'Th-234': -2.6140879622245746e-27, 'Tl-206': -4.332210492987691e-34,
     'Tl-210': 2.2028710112960294e-31, 'U-234': -1.0389580591195201e-26,
     'U-238': -8.466705440297454e-27}

All the progeny of Es-254 should have an activity of exactly zero for this
calculation.

``radioactivedecay`` thus offers a decay calculation mode using SymPy
:ref:`[4] <refs>` arbitrary precision computation routines for when high
numerical precision is needed:

.. code-block:: python3

    >>> inv = rd.InventoryHP({'Es-254': 1.0})
    >>> inv.activities()
    {'At-218': 0.0, 'Bi-210': 0.0,
     'Bi-214': 0.0, 'Bk-250': 0.0,
     'Cf-250': 0.0, 'Cm-246': 0.0,
     'Es-254': 1.0, 'Fm-254': 0.0,
     'Hg-206': 0.0, 'Pa-234': 0.0,
     'Pa-234m': 0.0, 'Pb-206': 0.0,
     'Pb-210': 0.0, 'Pb-214': 0.0,
     'Po-210': 0.0, 'Po-214': 0.0,
     'Po-218': 0.0, 'Pu-242': 0.0,
     'Ra-226': 0.0, 'Rn-218': 0.0,
     'Rn-222': 0.0, 'Th-230': 0.0,
     'Th-234': 0.0, 'Tl-206': 0.0,
     'Tl-210': 0.0, 'U-234': 0.0,
     'U-238': 0.0}

The ``InventoryHP`` class ``decay()`` method carries exact SymPy expressions
through decay calculations as far as is practicable. At the final step, the
decayed activity for each radionuclide is evaluated to high numerical precision
and cast to a double-precision float to return the decayed ``Inventory``.

In practice using SymPy to exactly evaluate the exponential terms in the above
analytical solution to the radionuclide decay equations can be very time
consuming. Therefore by default the exponential terms are evaluated numerically
to 320 significant figures of precision mid-decay calculation. Empirically this
was found to give results for a range of test decay calculations, i.e. using a
higher number of significant figures offered no improvement in the numerical
accuracy of the results after the outputs are cast to double-precision floats.
You can also select your own number of significant figures for the calculation
by setting the ``InventoryHP.sig_fig`` attribute of the ``InventoryHP``
instance.

References
----------

1. M Amaku, PR Pascholati & VR Vanin, Comp. Phys. Comm. 181, 21-23 (2010). DOI: `10.1016/j.cpc.2009.08.011 <https://doi.org/10.1016/j.cpc.2009.08.011>`_
2. ICRP Publication 107: Nuclear Decay Data for Dosimetric Calculations. Ann. ICRP 38 (3), 1-96 (2008). `PDF <https://journals.sagepub.com/doi/pdf/10.1177/ANIB_38_3>`_
3. RI Balkin et al. Atomic Energy 123, 406-411 (2018). `10.1007/s10512-018-0360-2 <https://doi.org/10.1007/s10512-018-0360-2>`_
4. A Meurer et al. PeerJ Comp. Sci. 3, e103 (2017). DOI: `10.7717/peerj-cs.103 <https://doi.org/10.7717/peerj-cs.103>`_
