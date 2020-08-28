Using radioactivedecay
======================

Importing the package in Python
-------------------------------
    
Import the ``radioactivedecay`` package by:

.. code-block:: python3

    >>> import radioactivedecay as rd

Creating inventories of radionuclides
-------------------------------------

Create an inventory of radionuclides and associated activities as follows:

.. code-block:: python3

    >>> inv_t0 = rd.Inventory({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005})

The following commands can be used to view the contents (radionuclides and
their actitivites) and decay data set associated with an inventory:

.. code-block:: python3

    >>> inv_t0.contents
    {'U-234': 0.005, 'U-235': 0.72, 'U-238': 99.274}
    >>> inv_t0.radionuclides
    ['U-234', 'U-235', 'U-238']
    >>> inv_t0.activities
    [0.005, 0.72, 99.274]

Radioactive decay calculations
------------------------------

Use ``decay()`` to decay the natural uranium inventory for a billion years:

.. code-block:: python3

    >>> inv_t1 = inv_t0.decay(1E9, 'y')
    >>> inv_t1.contents
    {'Ac-227': 0.2690006281740556, 'At-218': 0.017002868638497183,
     'At-219': 2.227325201281319e-07, 'Bi-210': 85.01434361515662,
     'Bi-211': 0.26900084425585846, 'Bi-214': 85.01432618961896,
     'Bi-215': 2.1605054452429237e-07, 'Fr-223': 0.0037122086688021884,
     'Hg-206': 1.6152725286830197e-06, 'Pa-231': 0.2690006198549055,
     'Pa-234': 0.13601313171698984, 'Pa-234m': 85.00820732310412,
     'Pb-210': 85.01434361489548, 'Pb-211': 0.2690008442558569,
     'Pb-214': 84.99734032384839, 'Po-210': 85.01434362236536,
     'Po-211': 0.0007424423301461693, 'Po-214': 84.99649018398776,
     'Po-215': 0.26900084425583065, 'Po-218': 85.01434319248591,
     'Ra-223': 0.26900062820528614, 'Ra-226': 85.01434319228659,
     'Rn-218': 1.7002868638497185e-05, 'Rn-219': 0.26900062820528614,
     'Rn-222': 85.0143431924858, 'Th-227': 0.2652884195245263,
     'Th-230': 85.01431274847525, 'Th-231': 0.26898810215560653,
     'Th-234': 85.00820732310407, 'Tl-206': 0.00011383420610068998,
     'Tl-207': 0.26825840192571576, 'Tl-210': 0.01785300849981999,
     'U-234': 85.01287846492669, 'U-235': 0.2689881021544942,
     'U-238': 85.00820732184867}
    
``decay()`` takes two arguments: the decay time period and its units. The units
can be entered using :code:`'s'`, :code:`'m'`, :code:`'h'`, :code:`'d'`,
:code:`'y'` for seconds, minutes, hours, days and years, respectively.

Radionuclide name formatting and metastable states
--------------------------------------------------

Radionuclides can be specified in three different ways. The following are all
equivalent ways to specify radon-222:

.. code-block:: python3

    >>> inv = rd.Inventory({'Rn-222': 1.0})
    >>> inv = rd.Inventory({'Rn222': 1.0})
    >>> inv = rd.Inventory({'222Rn': 1.0})

First and second metastable states of radionuclides can be inputted using
\'m\' and \'n\', respectively, i.e.:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'Ir-192m': 1.0})
    >>> inv2 = rd.Inventory({'Ir-192n': 1.0})

Equivalently you could have specified these metastable states using
:code:`'Ir192m'`, :code:`'192mIr'`, :code:`'Ir192n'` or :code:`'192nIr'`.

Adding and removing radionuclides
---------------------------------

It is easy to add radionuclides to inventories using the ``add()`` method:

.. code-block:: python3

    >>> inv = rd.Inventory({'H-3': 1.0, 'Be-10': 2.0})
    >>> inv.contents
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.add({'C-14': 3.0, 'K-40': 4.0})
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0}

Likewise use ``remove()`` to erase one or more radionuclides from an inventory:

.. code-block:: python3

    >>> inv.remove('H-3')
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'K-40': 4.0}
    >>> inv.remove(['Be-10', 'K-40'])
    >>> inv.contents
    {'C-14': 3.0}

Inventory arithmetic
--------------------

You can add the conents of different inventories together to create a new
inventory:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'H-3': 1.0})
    >>> inv2 = rd.Inventory({'C-14': 1.0})
    >>> inv = inv1 + inv2
    >>> inv.contents
    {'C-14': 1.0, 'H-3': 1.0}

It is also possible to subtract the contents of one inventory from another:

.. code-block:: python3

    >>> inv = inv - inv1
    >>> inv.contents
    {'C-14': 1.0, 'H-3': 0.0}

Multiplication and division on inventories
------------------------------------------

You can multipy or divide the activites of all radionuclides in an inventory
by a constant as follows:

.. code-block:: python3

    >>> inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0})
    >>> inv = inv * 2
    >>> inv.contents
    {'Sr-90': 2.0, 'Cs-137': 2.0}
    >>> inv = inv / 2
    >>> inv.contents
    {'Sr-90': 1.0, 'Cs-137': 1.0} 

Decay data for individual radionuclides
---------------------------------------

Use to ``Radionuclide`` class to obtain decay data for individual
radionuclides. For example, to get the half-life of Rn-222:

.. code-block:: python3

    >>> Rn222 = rd.Radionuclide('Rn-222')
    >>> Rn222.half_life('d')
    3.8235

The argument for the ``half_life()`` method is your desired time unit for the
outputted half-life. The default if not specified is seconds.
