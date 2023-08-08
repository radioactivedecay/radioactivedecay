Tutorial
========

Importing the package in Python
-------------------------------
    
Import the ``radioactivedecay`` package by:

.. code-block:: python3

    >>> import radioactivedecay as rd

Creating inventories of nuclides
--------------------------------

Create an inventory of nuclides as follows:

.. code-block:: python3

    >>> inv_t0 = rd.Inventory({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005}, 'mol')

This is an inventory of natural uranium. The amounts of each nuclide were
specified in moles.

Within the code, the ``Inventory`` class keeps track of the number of atoms of
each nuclide it contains. The following commands can be used to show the
contents in terms of activities, numbers of atoms, moles, masses, or
abundances:

.. code-block:: python3

    >>> inv_t0.activities('MBq')
    {'U-234': 269.4016050086039, 'U-235': 13.528246506057048, 'U-238': 293.90300567125}
    >>> inv_t0.nuclides
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
    Inventory activities (Bq): {'U-234': 269401605.0086039, 'U-235': 13528246.506057048, 'U-238': 293903005.67125}, decay dataset: icrp107_ame2020_nubase2020

By default the dictionary passed to the ``Inventory()`` constructor is assumed
to contain activities in Bq. The user can easily specify different units:

.. code-block:: python3

    # initialize an inventory using activities:
    >>> inv = rd.Inventory({'C-14': 5.0, 'H-3': 2.0})
    >>> inv.activities('Bq')
    {'C-14': 5.0, 'H-3': 2.0}
    >>> inv.numbers()
    {'C-14': 1297520091697.4946, 'H-3': 1121785791.5588164}
    
    # initialize an inventory using number of atoms:
    >>> inv = rd.Inventory({'U-238': 2000.0, 'U-235': 3000.0, 'U-234': 1500.0}, 'num')
    >>> inv.activities('Bq')
    {'U-234': 1.3420556696283726e-10, 'U-235': 9.360075764027427e-14, 'U-238': 9.832129719300668e-15}
    >>> inv.numbers()
    {'U-234': 1500.0, 'U-235': 3000.0, 'U-238': 2000.0}

It is also possible to create an inventory by reading directly from a CSV-type
file via the ``rd.read_csv()`` function. The file's first column should contain
the nuclides, and the second column the amount of each nuclide.

An optional third column can be provided with the unit, which can differ for
each nuclide. This makes it possible to load an inventory from mixed activity,
moles or mass units for each nuclide.

Example CSV file, saved as e.g. ``example_file.csv``:

.. code-block:: text

    nuclide|amount|units
    C-14|5.0|Ci
    H-3|0.2|g
    He-3|1|mol

Read command - ``skip_rows=1`` is required to ignore the header row:

.. code-block:: python3

    >>> inv = rd.read_csv('example_file.csv', delimiter='|', skip_rows=1)

Radioactive decay calculations
------------------------------

Use ``decay()`` to perform a radioactive decay calculation on the natural
uranium inventory:

.. code-block:: python3

    >>> inv_t1 = inv_t0.decay(1E9, 'y')
    >>> inv_t1.activities('Bq')
    {'Ac-227': 5054315.0114205815, 'At-218': 50337.39144073731,
     'At-219': 4.184972829456502, 'Bi-210': 251686958.45501313,
     'Bi-211': 5054319.0714315465, 'Bi-214': 251686906.8663001,
     'Bi-215': 4.059423644572891, 'Fr-223': 69749.54715760818,
     'Hg-206': 4.782052210630576, 'Pa-231': 5054314.855110146,
     'Pa-234': 402670.06690959306, 'Pa-234m': 251668791.81845263,
     'Pb-206': 0.0, 'Pb-207': 0.0,
     'Pb-210': 251686958.45423996, 'Pb-211': 5054319.071431517,
     'Pb-214': 251636619.8122487, 'Po-210': 251686958.47635475,
     'Po-211': 13949.920637151068, 'Po-214': 251634102.95324954,
     'Po-215': 5054319.071431024, 'Po-218': 251686957.20368654,
     'Ra-223': 5054315.01200738, 'Ra-226': 251686957.20309648,
     'Rn-218': 50.33739144073732, 'Rn-219': 5054315.01200738,
     'Rn-222': 251686957.20368624, 'Th-227': 4984565.464625097,
     'Th-230': 251686867.07347885, 'Th-231': 5054079.657163195,
     'Th-234': 251668791.81845245, 'Tl-206': 337.00883737124855,
     'Tl-207': 5040369.15079446, 'Tl-210': 52854.250441923046,
     'U-234': 251682620.8433893, 'U-235': 5054079.657142295,
     'U-238': 251668791.8147358}
        
The ``decay()`` method takes two arguments: the decay time period and its
units. Units can be entered using :code:`'ps'`, :code:`'ns'`, :code:`'us'`,
:code:`'ms'`, :code:`'s'`, :code:`'m'`, :code:`'h'`, :code:`'d'`, :code:`'y'`,
:code:`'ky'`, :code:`'My'`, :code:`'Gy'`, :code:`'Ty'` and :code:`'Py'` for
picoseconds, nanoseconds, microseconds, milliseconds, seconds, minutes, hours,
days, years, kiloyears, megayears, gigayears, terayears and petayears,
respectively. In the above case we decayed for one billion years.

High numerical precision radioactive decay calculations
-------------------------------------------------------

The ``InventoryHP`` class can be used for high numerical precision
calculations. This class uses SymPy arbitrary-precision numerical calculation
routines. The ``InventoryHP.decay()`` method can give more accurate decay
calculation results for chains containing radionuclides with long and short
half-lives, or when extremely long or short decay times are required. Note
computation times are longer when using the ``InventoryHP`` class as compared
to the ``Inventory`` class.

.. code-block:: python3

    >>> high_precision_inv_t0 = rd.InventoryHP({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005}, 'mol')
    >>> high_precision_inv_t1 = high_precision_inv_t0.decay(1E9, 'y')
    >>> high_precision_inv_t1.activities()
    {'Ac-227': 5054315.0114205815, 'At-218': 50337.391440737316,
     'At-219': 4.184972829456501, 'Bi-210': 251686958.4550132,
     'Bi-211': 5054319.071431547, 'Bi-214': 251686906.86630014,
     'Bi-215': 4.059423644572889, 'Fr-223': 69749.54715760818,
     'Hg-206': 4.782052210630577, 'Pa-231': 5054314.855110147,
     'Pa-234': 402670.0669095932, 'Pa-234m': 251668791.81845266,
     'Pb-206': 0.0, 'Pb-207': 0.0,
     'Pb-210': 251686958.45424002, 'Pb-211': 5054319.071431518,
     'Pb-214': 251636619.8122487, 'Po-210': 251686958.4763548,
     'Po-211': 13949.92063715107, 'Po-214': 251634102.95324966,
     'Po-215': 5054319.071431025, 'Po-218': 251686957.2036866,
     'Ra-223': 5054315.01200738, 'Ra-226': 251686957.20309657,
     'Rn-218': 50.33739144073732, 'Rn-219': 5054315.012007381,
     'Rn-222': 251686957.20368624, 'Th-227': 4984565.464625096,
     'Th-230': 251686867.07347894, 'Th-231': 5054079.657163196,
     'Th-234': 251668791.81845254, 'Tl-206': 337.0088373712486,
     'Tl-207': 5040369.150794461, 'Tl-210': 52854.25044192306,
     'U-234': 251682620.84338942, 'U-235': 5054079.6571422955,
     'U-238': 251668791.8147359}

Calculating total number of decays
----------------------------------

The ``cumulative_decays()`` method can be used to calculate the total number
of decays that occur for each radionuclide over a decay period. With a normal
precision ``Inventory``:

.. code-block:: python3

    >>> inv = rd.Inventory({'Sr-90': 10.0}, 'num')
    >>> inv.cumulative_decays(1.0 'My')
    {'Sr-90': 10.0, 'Y-90': 10.000000000000002}

So in this calculation, 10 atoms of strontium-90 and 10 atoms of its progeny,
yttrium-90, decayed over the million year time period.

Using a high precision inventory fixes the floating-point rounding error:

.. code-block:: python3

    >>> inv = rd.InventoryHP({'Sr-90': 10.0}, 'num')
    >>> inv.cumulative_decays(1.0 'My')
    {'Sr-90': 10.0, 'Y-90': 10.0}

Note the ``cumulative_decays()`` method does not report the total number of
decays of stable nuclides (as these are all zero).

Nuclide name formatting and metastable states
--------------------------------------------------

Nuclides can be specified in four equivalent ways. These are all
equivalent ways of creating an inventory of radon-222:

.. code-block:: python3

    >>> inv = rd.Inventory({'Rn-222': 1.0})
    >>> inv = rd.Inventory({'Rn222': 1.0})
    >>> inv = rd.Inventory({'222Rn': 1.0})
    >>> inv = rd.Inventory({862220000: 1.0})

For the last instance, the 'canonical id' of the nuclide was used. This number is
in zzzaaammmm format, where the leftmost digits are the atomic number of radon,
the next three digits are its atomic mass number, and the last four are for
specifing its metastability. For nuclides with atomic mass numbers less than 100,
zeroes must be included as placeholders (ex. aaa = 003 for H-3). 

Metastable states of nuclides can be inputted by appending \'m\', \'n\', etc.
to the nuclide string, or 0001, 0002, etc. to the id, for first, second...
metastable states, respectively:

.. code-block:: python3

    # using nuclide strings:
    >>> inv = rd.Inventory({'Ir-192m': 1.0})
    >>> inv = rd.Inventory({'Ir-192n': 1.0})

    # or, equivalently, using canonical ids:
    >>> inv = rd.Inventory({771920001: 1.0})
    >>> inv = rd.Inventory({771920002: 1.0})

Equivalently we could have specified these metastable states using
:code:`'Ir192m'` or :code:`'192mIr'` for Ir-192m, or :code:`'Ir192n'` or
:code:`'192nIr'` for Ir-192n.

Note canonical ids are also used by `PyNE
<https://pyne.io/usersguide/nucname.html>`_.

Fetching atomic and decay data
------------------------------

The ``Nuclide`` class can be used to obtain atomic data for any specific nuclide,
and decay data for radionuclides. They are built similarly to inventories:

.. code-block:: python3

    >>> nuc = rd.Nuclide('Rn-222')
    >>> nuc = rd.Nuclide('Rn222')
    >>> nuc = rd.Nuclide('222Rn')
    >>> nuc = rd.Nuclide(862220000)

The atomic data for a nuclide can be accessed through the ``Nuclide`` object's
``Z``, ``A`` and ``atomic_mass`` methods:

.. code-block:: python3

    >>> nuc = rd.Nuclide('K-40')
    >>> nuc.Z  # proton number
    19
    >>> nuc.A  # nucleon number
    40
    >>> nuc.atomic_mass  # atomic mass in g/mol
    39.963998165
    
Additionally, the canonical id of a nuclide, in zzzaaammmm format, can be
retrieved using the ``id`` method:

.. code-block:: python3

    >>> nuc = rd.Nuclide('Co-58m')
    >>> nuc.id
    270580001
    
Decay data for radionuclides can also be accessed using ``Nuclide`` objects.
For example, to get the half-life of iodine-123:

.. code-block:: python3

    >>> nuc = rd.Nuclide('I123')
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
to obtain the progeny, branching fractions and decay modes of a radionuclide:

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

Decay data can be accessed for all nuclides in an ``Inventory`` by using the
``half_lives()``, ``progeny()``, ``branching_fractions()`` and
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

    >>> rd.DEFAULTDATA.dataset_name
    'icrp107_ame2020_nubase2020'
    >>> rd.DEFAULTDATA.half_life('Cs-137', 'y')
    30.1671
    >>> rd.DEFAULTDATA.branching_fraction('Cs-137', 'Ba-137m')
    0.94399
    >>> rd.DEFAULTDATA.decay_mode('Cs-137', 'Ba-137m')
    'β-'


Adding and removing nuclides from inventories
---------------------------------------------

It is easy to add nuclides to an ``Inventory`` using the ``add()`` method:

.. code-block:: python3

    >>> inv = rd.Inventory({'H-3': 1.0, 'Be-10': 2.0})
    >>> inv.activities()
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.add({'C-14': 3.0, 'K-40': 4.0})
    >>> inv.activities()
    {'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0}

Similarly, subtract nuclides from an ``Inventory`` using the ``subtract()``
method:

.. code-block:: python3

    >>> inv.subtract({'Be-10': 1.0, 'K-40': 2.0})
    >>> inv.activities()
    {'Be-10': 1.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 2.0}

Likewise use ``remove()`` to erase one or more nuclide from an ``Inventory``:

.. code-block:: python3

    >>> inv.remove('H-3')
    >>> inv.activities()
    {'Be-10': 1.0, 'C-14': 3.0, 'K-40': 2.0}
    >>> inv.remove(['Be-10', 'K-40'])
    >>> inv.activities()
    {'C-14': 3.0}

The ``add()`` and ``subtract()`` methods also accept the ``'unit'`` argument
for inputs other than activities, and mixing input types is allowed:

.. code-block:: python3

    >>> inv.add({'H-3': 1.3E9}, 'num')
    >>> inv.activities()
    {'C-14': 3.0, 'H-3': 2.3177330463306007}
    >>> inv.subtract({'C-14': 7.1E-12}, 'g')
    >>> inv.activities()
    {'C-14': 1.8233790683016682, 'H-3': 2.3177330463306007}

You can also supply ``Nuclide`` objects instead of strings to the
``Inventory`` constructor, and the ``add()`` and ``remove()`` methods:

.. code-block:: python3

    >>> H3 = rd.Nuclide('H-3')
    >>> inv = rd.Inventory({H3: 1.0})
    >>> inv.activities()
    {'H-3': 1.0}
    >>> Be10 = rd.Nuclide('Be-10')
    >>> inv.add({Be10: 2.0})
    >>> inv.activities()
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.remove(H3)
    >>> inv.activities()
    {'Be-10': 2.0}

Note if the decay dataset of the ``Nuclide`` instance is different to that of
the ``Inventory`` instance, the former will be ignored and the existing decay
dataset of the ``Inventory`` will be used instead.

Inventory arithmetic
--------------------

You can add the contents of different inventories together to create a new
inventory:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'H-3': 1.0}, 'g')
    >>> inv2 = rd.Inventory({'C-14': 1.0}, 'g')
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

You can multiply or divide the amounts of all nuclides in an inventory by a
constant as follows:

.. code-block:: python3

    >>> inv = rd.Inventory({'Sr-90': 1.0, 'Cs-137': 1.0}, 'num')
    >>> inv = 2*inv
    >>> inv.numbers()
    {'Sr-90': 2.0, 'Cs-137': 2.0}
    >>> inv = inv / 2
    >>> inv.numbers()
    {'Sr-90': 1.0, 'Cs-137': 1.0} 

