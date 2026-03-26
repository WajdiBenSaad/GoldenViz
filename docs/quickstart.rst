Quickstart
==========

GoldenViz supports two main workflows.

Manual check
------------

.. code-block:: python

   import matplotlib.pyplot as plt
   import GoldenViz as gv

   fig, ax = plt.subplots()
   ax.plot([2021, 2022, 2023], [10, 14, 13])
   ax.set_title("Revenue trend")
   ax.set_xlabel("Year")
   ax.set_ylabel("Revenue (M€)")

   gv.check(fig)

Automatic mode in notebooks
---------------------------

.. code-block:: python

   import GoldenViz as gv
   gv.auto()

After ``gv.auto()`` is enabled, GoldenViz displays a notebook report below each new Matplotlib chart.
