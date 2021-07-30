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

    >>> inv_t0 = rd.Inventory({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005}, 'mol')

This is an inventory of natural uranium.

The ``Inventory`` class keeps track of the number of atoms
of each nuclide. The following commands can be used to convert the contents
(the nuclides and their respective number of atoms) into activities, numbers,
masses, or abundances, as well as return the decay data set associated with an
inventory:

.. code-block:: python3

    >>> inv_t0.activities('MBq')
    {'U-234': 269.4016050086039, 'U-235': 13.528246506057048, 'U-238': 293.90300567125}
    >>> inv_t0.radionuclides
    ['U-234', 'U-235', 'U-238']
    >>> inv_t0.numbers()
    {'U-234': 3.01107038e+21, 'U-235': 4.3359413471999995e+23, 'U-238': 5.9784200180824e+25}
    >>> inv_t0.masses('g')
    {'U-234': 1.17020475148, 'U-235': 169.23162824424, 'U-238': 23632.253822284463}
    >>> inv_t0.mass_fractions()
    {'U-234': 4.916278117985593e-05, 'U-235': 0.007109779290811992, 'U-238': 0.992841057928008}
    >>> inv_t0.moles()
    {'U-234': 0.005, 'U-235': 0.72, 'U-238': 99.274}
    >>> inv_t0.mole_fractions()
    {'U-234': 5.000050000500006e-05, 'U-235': 0.0072000720007200075, 'U-238': 0.992749927499275}
    >>> inv_t0
    Inventory activities (Bq): {'U-234': 269401605.0086039, 'U-235': 13528246.506057048, 'U-238': 293903005.67125}, decay dataset: icrp107

By default the input dictionary to ``Inventory()`` is assumed to contain
activities in Bq. The user can easily specify different units:

.. code-block:: python3

    # initialize an inventory using activities:
    >>> inv1 = rd.Inventory({'C-14': 5.0, 'H-3': 2.0})
    >>> inv1.activities('Bq')
    {'C-14': 5.0, 'H-3': 2.0}
    >>> inv1.numbers():
    {'C-14': 1297520091697.4946, 'H-3': 1121785791.5588164}
    
    # initialize an inventory using number of atoms:
    >>> inv2 = rd.Inventory({'U-238': 2000.0, 'U-235': 3000.0, 'U-234': 1500.0}, "num")
    >>> inv2.activities()
    {'U-234': 1.3420556696283726e-10, 'U-235': 9.360075764027427e-14, 'U-238': 9.832129719300668e-15}
    >>> inv2.numbers():
    {'U-234': 1500.0, 'U-235': 3000.0, 'U-238': 2000.0}


Radioactive decay calculations
------------------------------

Use ``decay()`` to perform a radioactive decay calculation on the natural
uranium inventory:

.. code-block:: python3

    >>> inv_t1 = inv_t0.decay(1E9, 'y')
    >>> inv_t1.activities()
    {'Ac-227': 5.054315011420582, 'At-218': 0.05033739144073731,
     'At-219': 4.184972829456502e-06, 'Bi-210': 251.68695845501313,
     'Bi-211': 5.0543190714315465, 'Bi-214': 251.68690686630012,
     'Bi-215': 4.059423644572891e-06, 'Fr-223': 0.06974954715760817,
     'Hg-206': 4.782052210630577e-06, 'Pa-231': 5.054314855110146,
     'Pa-234': 0.40267006690959306, 'Pa-234m': 251.66879181845263,
     'Pb-206': 0.0, 'Pb-207': 0.0,
     'Pb-210': 251.68695845423997, 'Pb-211': 5.054319071431516,
     'Pb-214': 251.6366198122487, 'Po-210': 251.68695847635476,
     'Po-211': 0.013949920637151067, 'Po-214': 251.63410295324954,
     'Po-215': 5.054319071431024, 'Po-218': 251.68695720368655,
     'Ra-223': 5.05431501200738, 'Ra-226': 251.68695720309648,
     'Rn-218': 5.033739144073732e-05, 'Rn-219': 5.05431501200738,
     'Rn-222': 251.68695720368623, 'Th-227': 4.9845654646250965,
     'Th-230': 251.68686707347885, 'Th-231': 5.054079657163196,
     'Th-234': 251.66879181845243, 'Tl-206': 0.00033700883737124854,
     'Tl-207': 5.040369150794461, 'Tl-210': 0.052854250441923045,
     'U-234': 251.68262084338932, 'U-235': 5.054079657142295,
     'U-238': 251.6687918147358}
        
The ``decay()`` method takes two arguments: the decay time period and its
units. Units can be entered using :code:`'ps'`, :code:`'ns'`, :code:`'us'`,
:code:`'ms'`, :code:`'s'`, :code:`'m'`, :code:`'h'`, :code:`'d'`, :code:`'y'`,
:code:`'ky'`, :code:`'My'`, :code:`'Gy'`, :code:`'Ty'` and :code:`'Py'` for
picoseconds, nanoseconds, microseconds, milliseconds, seconds, minutes, hours,
days, years, kiloyears, megayears, gigayears, terayears and petayears,
respectively. In the above case we decayed for one billion years.

High numerical precision radioactive decay calculations
-------------------------------------------------------

The ``decay_high_precision()`` method calculates radioactive decays with high
numerical precision, based on SymPy arbitrary-precision routines. This method
method can give more accurate results for decay chains containing radionuclides
with both very long and very short half-lives, or when extremely long or short
decay times are required. Note computation times can be slightly longer than
with the ``decay()`` method.

.. code-block:: python3

    >>> inv_t1 = inv_t0.decay_high_precision(1E9, 'y')
    >>> inv_t1.activities()
    {'Ac-227': 5.054315011420582, 'At-218': 0.05033739144073731,
     'At-219': 4.1849728294565e-06, 'Bi-210': 251.68695845501315,
     'Bi-211': 5.0543190714315465, 'Bi-214': 251.68690686630015,
     'Bi-215': 4.059423644572889e-06, 'Fr-223': 0.06974954715760817,
     'Hg-206': 4.782052210630577e-06, 'Pa-231': 5.054314855110146,
     'Pa-234': 0.40267006690959317, 'Pa-234m': 251.6687918184527,
     'Pb-206': 0.0, 'Pb-207': 0.0,
     'Pb-210': 251.68695845423997, 'Pb-211': 5.054319071431518,
     'Pb-214': 251.6366198122487, 'Po-210': 251.6869584763548,
     'Po-211': 0.01394992063715107, 'Po-214': 251.63410295324965,
     'Po-215': 5.054319071431025, 'Po-218': 251.6869572036866,
     'Ra-223': 5.054315012007379, 'Ra-226': 251.68695720309654,
     'Rn-218': 5.033739144073731e-05, 'Rn-219': 5.05431501200738,
     'Rn-222': 251.6869572036862, 'Th-227': 4.9845654646250965,
     'Th-230': 251.68686707347894, 'Th-231': 5.054079657163196,
     'Th-234': 251.66879181845252, 'Tl-206': 0.00033700883737124854,
     'Tl-207': 5.0403691507944615, 'Tl-210': 0.05285425044192306,
     'U-234': 251.6826208433894, 'U-235': 5.054079657142295,
     'U-238': 251.66879181473587}

Radionuclide name formatting and metastable states
--------------------------------------------------

Radionuclides can be specified in three equivalent ways. These are all
equivalent ways of creating an inventory of radon-222:

.. code-block:: python3

    >>> inv = rd.Inventory({'Rn-222': 1.0})
    >>> inv = rd.Inventory({'Rn222': 1.0})
    >>> inv = rd.Inventory({'222Rn': 1.0})

Metastable states of radionuclides can be inputted by appending \'m\', \'n\',
etc. for first, second... metastable states, respectively:

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
    >>> nuc.half_life()
    47772.0

The default time unit is seconds if no time unit argument is supplied to
``half_life()``. 

If you do not know the natural time unit for expressing the radionuclide
half-life, supply ``'readable'`` as the time argument. A human-readable string
with the half-life and time unit is returned:

.. code-block:: python3

    >>> nuc.half_life('readable')
    '13.27 h'

Use the ``progeny()``, ``branching_fractions()`` and ``decay_modes()`` methods
to obtain the progeny, branching fractions and decay modes of the radionuclide:

.. code-block:: python3

    >>> nuc.progeny()
    ['Te-123', 'Te-123m']
    >>> nuc.branching_fractions()
    [0.99996, 4.442e-05]
    >>> nuc.decay_modes()
    ['EC', 'EC']
    
These methods return data for the direct progeny of the radionuclide. \'EC\' is
an abbreviation for electron capture decay.

The ``decay_modes()`` method reports each decay mode of the parent radionuclide
resulting in each progeny. The types of decay mode in the ICRP-107 dataset are
α (alpha decay), β- (beta minus decay), β+ (positron emission), EC (electron
capture), IT (isomeric transition) and SF (spontaneous fission). Note that the
decay mode string is not a comprehensive list of all the radiation types
released when the parent radionuclide decays. Other radiation types, such as
gamma rays, x-rays, decay electrons and Auger electrons, may also be released
due to various nuclear and atomic relaxation processes that follow α, β-, β+
etc. decays.

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

Decay data can also be accessed directly from the decay datasets. Query the
data in ICRP-107, which is the default dataset in ``radioactivedecay``, by:

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
    >>> inv.activities()
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.add({'C-14': 3.0, 'K-40': 4.0})
    >>> inv.activities()
    {'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0}

Similarly, subtract radionuclides from an ``Inventory`` using the
``subtract()`` method:

.. code-block:: python3

    >>> inv.subtract({'Be-10': 1.0, 'K-40': 2.0})
    >>> inv.activities()
    {'Be-10': 1.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 2.0}

Likewise use ``remove()`` to erase one or more radionuclide from an
``Inventory``:

.. code-block:: python3

    >>> inv.remove('H-3')
    >>> inv.activities()
    {'Be-10': 1.0, 'C-14': 3.0, 'K-40': 2.0}
    >>> inv.remove(['Be-10', 'K-40'])
    >>> inv.activities()
    {'C-14': 3.0}

The ``add()`` and ``subtract()`` methods also have the ``input_type`` argument
for inputs other than activities, and mixing input types is allowed:

.. code-block:: python3

    >>> inv.add({'H-3': 1.3E9}, input_type="numbers")
    >>> inv.activities()
    {'C-14': 3.0, 'H-3': 2.3177330463306007}
    >>> inv.subtract({'C-14': 7.1E-12}, input_type="masses")
    >>> inv.activities()
    {'C-14': 1.8233790683016682, 'H-3': 2.3177330463306007}

You can also supply ``Radionuclide`` objects instead of strings to the
``Inventory`` constructor, and the ``add()`` and ``remove()`` methods:

.. code-block:: python3

    >>> H3 = rd.Radionuclide('H-3')
    >>> inv = rd.Inventory({H3: 1.0})
    >>> inv.activities()
    {'H-3': 1.0}
    >>> Be10 = rd.Radionuclide('Be-10')
    >>> inv.add({Be10: 2.0})
    >>> inv.activities()
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.remove(H3)
    >>> inv.activities()
    {'Be-10': 2.0}

Note if the decay dataset of the ``Radionuclide`` instance is different to that
of the ``Inventory`` instance, the former will be ignored and the existing
decay dataset of the ``Inventory`` will be used instead.

Inventory arithmetic
--------------------

You can add the contents of different inventories together to create a new
inventory:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'H-3': 1.0}, input_type="masses")
    >>> inv2 = rd.Inventory({'C-14': 1.0}, input_type="masses")
    >>> inv = inv1 + inv2
    >>> inv.masses()
    {'C-14': 1.0, 'H-3': 1.0}

It is also possible to subtract the contents of one inventory from another:

.. code-block:: python3

    >>> inv = inv - inv1
    >>> inv.masses()
    {'C-14': 1.0, 'H-3': 0.0}

Multiplication and division on inventories
------------------------------------------

You can multiply or divide the activities of all radionuclides in an inventory
by a constant as follows:

.. code-block:: python3

    >>> inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0}, input_type="numbers")
    >>> inv = inv * 2
    >>> inv.numbers()
    {'Sr-90': 2.0, 'Cs-137': 2.0}
    >>> inv = inv / 2
    >>> inv.numbers()
    {'Sr-90': 1.0, 'Cs-137': 1.0} 

