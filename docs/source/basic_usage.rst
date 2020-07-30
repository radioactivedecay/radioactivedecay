Basic Usage
===========
    
Importing in Python
-------------------
    
Import the ``radioactivedecay`` package in Python via:

.. code-block:: python3

    >>> import radioactivedecay as rd

Creating and decaying inventories of radionuclides
--------------------------------------------------

Create an inventory of radionuclides and their activities as follows:

.. code-block:: python3

    >>> inv_t0 = rd.Inventory({'U-238': 99.274, 'U-235': 0.720, 'U-234': 0.005})

Decay the inventory by 1.5 years and show the new activities:

.. code-block:: python3

    >>> inv_t1 = inv_t0.decay(1.5, 'y')
    >>> inv_t1.contents
    {'Ac-227': 5.340603357904309e-07, 'At-218': 4.487750070853225e-15,
    'At-219': 4.4216505884111565e-13, 'Bi-210': 3.3130807422178877e-13,
    'Bi-211': 4.5541237150637006e-07, 'Bi-214': 2.2410641667189786e-11,
    'Bi-215': 4.2888824586560307e-13, 'Fr-223': 7.369442676365442e-09,
    'Hg-206': 6.202044386326762e-21, 'Pa-231': 2.2786660561135543e-05,
    'Pa-234': 0.1588383769120255, 'Pa-234m': 99.27398573690083,
    'Pb-210': 3.475229846217194e-13, 'Pb-211': 4.5541620881157545e-07,
    'Pb-214': 2.2419792268541547e-11, 'Po-210': 1.5676334556892386e-13,
    'Po-211': 1.2569381029724905e-09, 'Po-214': 2.2403231179646845e-11,
    'Po-215': 4.5548094198406856e-07, 'Po-218': 2.245111011290413e-11,
    'Ra-223': 4.554806312479419e-07, 'Ra-226': 2.2940210201589685e-11,
    'Rn-218': 4.4904161775053266e-18, 'Rn-219': 4.5548051312434185e-07,
    'Rn-222': 2.246679742980326e-11, 'Th-227': 4.776273033743675e-07,
    'Th-230': 7.15195428871165e-08, 'Th-231': 0.7199999989396266,
    'Th-234': 99.27398573738093, 'Tl-206': 4.7413013901286e-19,
    'Tl-207': 4.54146903777397e-07, 'Tl-210': 4.709672889168785e-15,
    'U-234': 0.005393731386900624, 'U-235': 0.7199999989366492,
    'U-238': 99.27399997689857}
    
Time units can be expressed in :code:`'s'`, :code:`'m'`, :code:`'h'`,
:code:`'d'`, :code:`'y'` etc.
    
Adding and removing from inventories
------------------------------------

It is easy to add and remove radionuclides from inventories:

.. code-block:: python3

    >>> inv = rd.Inventory({'H-3': 1.0, 'Be-10': 2.0})
    >>> inv.contents
    {'Be-10': 2.0, 'H-3': 1.0}
    >>> inv.add({'C-14': 3.0, 'K-40': 4.0})
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'H-3': 1.0, 'K-40': 4.0}
    >>> inv.remove('H-3')
    >>> inv.contents
    {'Be-10': 2.0, 'C-14': 3.0, 'K-40': 4.0}
    >>> inv.remove(['Be-10', 'K-40'])
    >>> inv.contents
    {'C-14': 3.0}

You can also add and subtract inventories by:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'H-3': 1.0})
    >>> inv2 = rd.Inventory({'C-14': 1.0})
    >>> inv = inv1 + inv2
    >>> inv.contents
    {'C-14': 1.0, 'H-3': 1.0}
    >>> inv = inv - inv2
    >>> inv.contents
    {'C-14': 1.0, 'H-3': 0.0}

Radionuclide string formatting and metastable states
----------------------------------------------------

``radioactivedecay`` supports radionuclide strings formatted in three ways,
hence the following are all equivalent:

.. code-block:: python3

    >>> inv = rd.Inventory({'Rn-222': 1.0})
    >>> inv = rd.Inventory({'Rn222': 1.0})
    >>> inv = rd.Inventory({'222Rn': 1.0})

First and second metastable states of radionuclides can be inputted using
\'m\' and \'n\' respectively, i.e.:

.. code-block:: python3

    >>> inv1 = rd.Inventory({'Ir-192m': 1.0})
    >>> inv2 = rd.Inventory({'Ir-192n': 1.0})

Equivalently these metastable states could have been specified using
:code:`'Ir192m'`, :code:`'192mIr'`, :code:`'Ir192n'` or :code:`'192nIr'`.

Fetching decay data
-------------------

``radioactivedecay`` includes a ``Radionuclide`` class to fetch the decay data
for individual radionuclides. To get a half-life of a radionuclide:

.. code-block:: python3

    >>> Rn222 = rd.Radionuclide('Rn-222')
    >>> Rn222.halflife('d')
    3.8235

