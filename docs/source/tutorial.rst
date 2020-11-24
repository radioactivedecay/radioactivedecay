Tutorial
========

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

This is an inventory of natural uranium.

The following commands can be used to view the contents (the radionuclides and
their activities) and decay data set associated with an inventory:

.. code-block:: python3

    >>> inv_t0.contents
    {'U-234': 0.005, 'U-235': 0.72, 'U-238': 99.274}
    >>> inv_t0.radionuclides
    ['U-234', 'U-235', 'U-238']
    >>> inv_t0.activities
    [0.005, 0.72, 99.274]
    >>> inv_t0
    Inventory: {'U-234': 0.005, 'U-235': 0.72, 'U-238': 99.274}, decay dataset: icrp107

Radioactive decay calculations
------------------------------

Use ``decay()`` to perform a radioactive decay calculation on the natural
uranium inventory:

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
    
The ``decay()`` method takes two arguments: the decay time period and its
units. Units can be entered using :code:`'ns'`, :code:`'us'`, :code:`'ms'`,
:code:`'s'`, :code:`'m'`, :code:`'h'`, :code:`'d'`, :code:`'y'`, :code:`'ky'`,
:code:`'My'`, :code:`'Gy'`, :code:`'Ty'` and :code:`'Py'` for nanoseconds,
microseconds, milliseconds, seconds, minutes, hours, days, years, kiloyears,
megayears, gigayears, terayears and petayears, respectively. In the above case
we decayed for one billion years.

Radionuclide name formatting and metastable states
--------------------------------------------------

Radionuclides can be specified in three equivalent ways. These all give
radon-222:

.. code-block:: python3

    >>> inv = rd.Inventory({'Rn-222': 1.0})
    >>> inv = rd.Inventory({'Rn222': 1.0})
    >>> inv = rd.Inventory({'222Rn': 1.0})

Metastable states of radionuclides can be inputted using \'m\', \'n\', etc. for
first, second... metastable states, respectively:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'Ir-192m': 1.0})
    >>> inv2 = rd.Inventory({'Ir-192n': 1.0})

Equivalently we could have specified these metastable states using
:code:`'Ir192m'` or :code:`'192mIr'` for the former, or :code:`'Ir192n'` or
:code:`'192nIr'` for the latter.

Fetching decay data
-------------------

The ``Radionuclide`` class can be used to obtain decay data for individual
radionuclides. For example, to get the half-life of iodine-123:

.. code-block:: python3

    >>> nuc = rd.Radionuclide('I123')
    >>> nuc.half_life('d')
    13.27

The argument for the ``half_life()`` method is your desired time unit for the
output. The default is seconds if no unit is specified.

Use the ``progeny()``, ``branching_fractions()`` and ``decay_modes()`` methods
to obtain the progeny, branching fractions and decay modes:

.. code-block:: python3

    >>> nuc.progeny()
    ['Te-123', 'Te-123m']
    >>> nuc.branching_fractions()
    [0.99996, 4.442e-05]
    >>> nuc.decay_modes()
    ['EC', 'EC']
    
The methods return data for the direct progeny of the radionuclide. \'EC\' is
the abbreviation for the electron capture decay mode.

The ``decay_modes()`` method reports the types of decay of the parent which
result in each progeny. The decay modes in the ICRP-107 dataset are \'α\'
(alpha decay), \'β-\' (beta minus decay), \'β+\' (positron emission), \'EC\'
(electron capture), \'IT\' (isomeric transition) and \'SF\' (spontaneous
fission). Note that a decay mode is not a comprehensive list of all the
radiation types released by the radionuclide decay. Be aware that other
radiation types, such as gamma rays, electrons and  x-rays, may be released
from parent to progeny decay mode with only a single label (e.g. \'α\', \'β-\'
or \'β+\').

Decay data can be accessed for all radionuclides in an ``Inventory``
by using the ``half_lives()``, ``progeny()``, ``branching_fractions()`` and
``decay_modes()`` methods:

.. code-block:: python3

    >>> inv = rd.Inventory({'C-14': 1.0, 'K-40': 2.0})
    >>> inv.half_lives('y')
    {'C-14': 5700.0, 'K-40': 1251000000.0}
    >>> inv.progeny()
    {'C-14': ['N-14'], 'K-40': ['Ca-40', 'Ar-40']}
    >>> inv.branching_fractions()
    {'C-14': [1.0], 'K-40': [0.8914, 0.1086]}
    >>> inv.decay_modes()
    {'C-14': ['β-'], 'K-40': ['β-', 'β+ & EC']}

Decay data can also be accessed directly from the decay datasets. To query the
data in ICRP-107, which is the default dataset in ``radioactivedecay``, use:

.. code-block:: python3

    >>> rd.DEFAULTDATA.dataset
    'icrp107'
    >>> rd.DEFAULTDATA.half_life('Cs-137', 'y')
    30.1671
    >>> rd.DEFAULTDATA.branching_fraction('Cs-137', 'Ba-137m')
    0.94399
    >>> rd.DEFAULTDATA.decay_mode('Cs-137', 'Ba-137m')
    'β-'


Adding and removing radionuclides from inventories
--------------------------------------------------

It is easy to add radionuclides to an ``Inventory`` using the ``add()`` method:

.. code-block:: python3

    >>> inv = rd.Inventory({'H-3': 1.0, 'Be-10': 2.0})
    >>> inv.contents
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.add({'C-14': 3.0, 'K-40': 4.0})
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0}

Likewise use ``remove()`` to erase one or more radionuclide from an
``Inventory``:

.. code-block:: python3

    >>> inv.remove('H-3')
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'K-40': 4.0}
    >>> inv.remove(['Be-10', 'K-40'])
    >>> inv.contents
    {'C-14': 3.0}

You can also supply ``Radionuclide`` objects instead of strings to the
``Inventory`` constructor, and the ``add()`` and ``remove()`` methods:

.. code-block:: python3

    >>> H3 = rd.Radionuclide('H-3')
    >>> inv = rd.Inventory({H3: 1.0})
    >>> inv.contents
    {'H-3': 1.0}
    >>> Be10 = rd.Radionuclide('Be-10')
    >>> inv.add({Be10: 2.0})
    >>> inv.contents
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.remove(H3)
    >>> inv.contents
    {'Be-10': 2.0}

Note if the decay dataset of the ``Radionuclide`` instance is different to that
of the ``Inventory`` instance, the former will be ignored and the existing
decay dataset of the ``Inventory`` will be used instead.

Inventory arithmetic
--------------------

You can add the contents of different inventories together to create a new
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

You can multiply or divide the activities of all radionuclides in an inventory
by a constant as follows:

.. code-block:: python3

    >>> inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0})
    >>> inv = inv * 2
    >>> inv.contents
    {'Sr-90': 2.0, 'Cs-137': 2.0}
    >>> inv = inv / 2
    >>> inv.contents
    {'Sr-90': 1.0, 'Cs-137': 1.0} 

