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

The ``decay_time_series_pandas()`` method can be used if, rather than just the values
at the end of the time period, access to finer resolution decay data is required. The
method runs ``decay()``, storing the data at each iteration and returning the
complete data set as a pandas dataframe. The only required argument is the decay
time period as a number, or as a numpy array with the individual decay times data
is needed for. Optional arguments are the decay time units in the same format as for
the ``decay()`` method, the decay units, whether the time scale should be linear or
logarithmic and, if the decay time is given as a float, how many decay points should be
calculated.

Using ``decay_time_series_pandas()`` to interrogate how the mass fraction of :sup:`14`\C decays over
20,000 years with :sup:`14`\N taking it's place. The default value for the number of point to calculate
is 501 so we will limit to 10 for this example

.. code-block:: python3

   >>> inv = Inventory({'C-14': 1.0})
   >>> inv.decay_time_series_pandas(time_period=20, time_units='ky', decay_units='mass_frac', npoints=10)
                  C-14      N-14
   Time (ky)                    
   0.000000   1.000000  0.000000
   2.222222   0.763204  0.236796
   4.444444   0.582480  0.417520
   6.666667   0.444550  0.555450
   8.888889   0.339282  0.660718
   11.111111  0.258941  0.741059
   13.333333  0.197624  0.802376
   15.555556  0.150827  0.849173
   17.777778  0.115112  0.884888
   20.000000  0.087854  0.912146

Or if we know the exact times for which we want to know the mass fractions, we can pass
a numpy array of those values:

.. code-block:: python3

   >>> import numpy as np
   >>> time_points = np.array([1.0, 4.5, 4.75, 5.0, 50.0])
   >>> inv.decay_time_series_pandas(time_period=time_points, time_units='ky', decay_units='mass_frac')
                  C-14      N-14
   Time (ky)                    
   1.00       0.885499  0.114501
   4.50       0.578558  0.421442
   4.75       0.561234  0.438766
   5.00       0.544429  0.455571
   50.00      0.002288  0.997712

Note that if you pass an array for the ``time_period`` as well as a value for ``npoints``, the
value specified by ``npoints`` will be silently ignored.

Once the data is stored in a pandas dataframe, we gain access to the `pandas <https://pandas.pydata.org/docs/user_guide/index.html>`_
ecosystem and the functionality on offer. For example, if we want to track the progeny, of a uranium compound
over time, but are only interested in those that are, or where, present above a certain number:

.. code-block:: python3

   # Initialize the inventory
   >>> inv = rd.Inventory({'U-238': 2000.0, 'U-235': 3000.0, 'U-234': 1500.0}, 'num')
   # Get the decay data for the required amount of time
   >>> df = inv.decay_time_series_pandas(time_period=1E9, time_units='y', decay_units='num', npoints=10)
   # Printing the dataframe to see what is originally created
   >>> df
                   Ac-227        At-218        At-219        Bi-210        Bi-211        Bi-214        Bi-215        Fr-223        Hg-206  ...    Th-230        Th-231        Th-234        Tl-206        Tl-207        Tl-210        U-234        U-235        U-238
   Time (y)                                                                                                                                ...                                                                                                                       
   0.000000e+00  0.000000  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  ...  0.000000  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  1500.000000  3000.000000  2000.000000
   1.111111e+08  0.000083  4.183008e-18  5.612824e-18  6.039192e-09  1.554277e-11  1.664837e-11  4.433329e-17  2.205038e-12  1.295477e-19  ...  0.033168  1.112054e-08  2.903132e-08  4.704880e-18  3.454878e-11  2.283922e-16     0.108020  2689.120153  1965.820782
   2.222222e+08  0.000075  4.111522e-18  5.031186e-18  5.935985e-09  1.393213e-11  1.636385e-11  3.973918e-17  1.976537e-12  1.273338e-19  ...  0.032601  9.968160e-09  2.853519e-08  4.624475e-18  3.096861e-11  2.244890e-16     0.106174  2410.455732  1932.225673
   3.333333e+08  0.000067  4.041257e-18  4.509821e-18  5.834541e-09  1.248839e-11  1.608420e-11  3.562115e-17  1.771716e-12  1.251577e-19  ...  0.032044  8.935193e-09  2.804754e-08  4.545445e-18  2.775944e-11  2.206526e-16     0.104360  2160.668362  1899.204692
   4.444444e+08  0.000060  3.972194e-18  4.042484e-18  5.734831e-09  1.119426e-11  1.580933e-11  3.192985e-17  1.588119e-12  1.230188e-19  ...  0.031496  8.009269e-09  2.756821e-08  4.467765e-18  2.488282e-11  2.168817e-16     0.102577  1936.765612  1866.748026
   5.555556e+08  0.000054  3.904311e-18  3.623575e-18  5.636825e-09  1.003423e-11  1.553915e-11  2.862107e-17  1.423547e-12  1.209165e-19  ...  0.030958  7.179296e-09  2.709708e-08  4.391413e-18  2.230430e-11  2.131753e-16     0.100824  1736.065147  1834.846033
   6.666667e+08  0.000048  3.837588e-18  3.248076e-18  5.540494e-09  8.994421e-12  1.527360e-11  2.565516e-17  1.276030e-12  1.188501e-19  ...  0.030429  6.435330e-09  2.663401e-08  4.316365e-18  1.999298e-11  2.095322e-16     0.099100  1556.162591  1803.489231
   7.777778e+08  0.000043  3.772005e-18  2.911489e-18  5.445809e-09  8.062360e-12  1.501258e-11  2.299660e-17  1.143799e-12  1.168190e-19  ...  0.029909  5.768458e-09  2.617884e-08  4.242600e-18  1.792117e-11  2.059514e-16     0.097407  1394.902728  1772.668305
   8.888889e+08  0.000039  3.707543e-18  2.609781e-18  5.352742e-09  7.226885e-12  1.475602e-11  2.061354e-17  1.025271e-12  1.148226e-19  ...  0.029398  5.170692e-09  2.573145e-08  4.170096e-18  1.606406e-11  2.024318e-16     0.095742  1250.353679  1742.374097
   1.000000e+09  0.000035  3.644182e-18  2.339338e-18  5.261266e-09  6.477987e-12  1.450384e-11  1.847743e-17  9.190258e-13  1.128603e-19  ...  0.028895  4.634871e-09  2.529171e-08  4.098830e-18  1.439940e-11  1.989723e-16     0.094106  1120.783759  1712.597605
   
   [10 rows x 37 columns]
   # Slice the result, keeping only those progeny that ever existed above a specific quantity
   >>> df.loc[:, df.max() > 100]
                      Pb-206       Pb-207        U-234        U-235        U-238
   Time (y)                                                                     
   0.000000e+00     0.000000     0.000000  1500.000000  3000.000000  2000.000000
   1.111111e+08  1534.039370   310.754872     0.108020  2689.120153  1965.820782
   2.222222e+08  1567.636948   589.432493     0.106174  2410.455732  1932.225673
   3.333333e+08  1600.660357   839.231695     0.104360  2160.668362  1899.204692
   4.444444e+08  1633.119409  1063.145051     0.102577  1936.765612  1866.748026
   5.555556e+08  1665.023749  1263.855025     0.100824  1736.065147  1834.846033
   6.666667e+08  1696.382856  1443.766102     0.099100  1556.162591  1803.489231
   7.777778e+08  1727.206048  1605.033604     0.097407  1394.902728  1772.668305
   8.888889e+08  1757.502483  1749.589500     0.095742  1250.353679  1742.374097
   1.000000e+09  1787.281165  1879.165558     0.094106  1120.783759  1712.597605

For more information on the use of dataframes, see the `pandas documentation
<https://pandas.pydata.org/docs/user_guide/index.html>`_.

To be consistent with the rest of the module, the method ``decay_time_series()`` is also provided and
this returns a tuple of a list and and dictionary containing the time elements and decay data
respectively.

.. code-block:: python3

   >>> inv = rd.Inventory({"C-14": 1.0})
   >>> times, data = inv.decay_time_series(time_period=20, time_units='ky', decay_units='mass_frac', npoints=5)
   >>> times
   [0.0, 5.0, 10.0, 15.0, 20.0]
   >>> data
   {'C-14': [1.0, 0.5444286529294111, 0.2964018201597633, 0.16136902316828455, 0.08785351725411072], 'N-14': [0.0, 0.45557134707058894, 0.7035981798402366, 0.8386309768317154, 0.9121464827458893]}

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

Writing results to a file
-------------------------

Similar to ``rd.read_csv()``, inventory objects have a ``.to_csv()`` method for
writing out the contents of an inventory to a CSV-type file. The user specifies
the filename, the units to be used, whether the units should be written into
the file (via the third column), the delimiter e.g. comma for a CSV file,
tab (``'\t'``) for a TSV file, and the header line for the file:

.. code-block:: python3

    >>> inv = rd.Inventory({'Cs-137': 1.02, 'Sr-90': 3.05}, 'Bq')
    >>> inv.to_csv('test_output.csv', units='mBq', delimiter='|', write_units=True, header=["nuclide", "quantity", "units"])

This produces a file named "test_output.csv" containing:

.. code-block:: text

    nuclide|amount|units
    Cs-137|1020.0|mBq
    Sr-90|3050.0|mBq
