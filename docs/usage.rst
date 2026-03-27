Usage
=====

Manual checks
-------------

Use :func:`GoldenViz.check` to analyze a specific figure and display the report.

.. code-block:: python

   import matplotlib.pyplot as plt
   import GoldenViz as gv

   fig, ax = plt.subplots()
   ax.plot([2021, 2022, 2023], [10, 14, 13])
   ax.set_title("Revenue trend")
   ax.set_xlabel("Year")
   ax.set_ylabel("Revenue (M€)")

   gv.check(fig)

If you do not have a reference to the figure, use :func:`GoldenViz.check_current`.

.. code-block:: python

   gv.check_current()

Automatic mode in Jupyter notebooks
-----------------------------------

GoldenViz can hook into Matplotlib so the report is displayed automatically under the chart.

.. code-block:: python

   import GoldenViz as gv
   gv.auto()

Once enabled, GoldenViz listens to Matplotlib display events and renders a notebook-friendly HTML report after each chart is shown.

To disable the automatic hook:

.. code-block:: python

   gv.disable()

Behavior outside notebooks
--------------------------

Outside Jupyter, GoldenViz falls back to text output in the terminal when ``display=True``.
