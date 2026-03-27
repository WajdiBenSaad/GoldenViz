Automatic mode
==============

GoldenViz can run automatically when a Matplotlib chart is rendered in a notebook.

Enable automatic mode
---------------------

.. code-block:: python

   import GoldenViz as gv
   gv.auto()

Disable automatic mode
----------------------

.. code-block:: python

   gv.disable()

Check whether automatic mode is active
--------------------------------------

.. code-block:: python

   gv.is_auto_enabled()

Expected behavior
-----------------

When automatic mode is active in Jupyter or VS Code notebooks, the chart is displayed first and the GoldenViz analysis panel appears directly below it.
