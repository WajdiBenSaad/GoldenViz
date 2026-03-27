Manual checks
=============

Use manual checks when you want explicit control over when GoldenViz runs.

Analyze and display a specific figure
-------------------------------------

.. code-block:: python

   gv.check(fig)

Analyze the current active figure
---------------------------------

.. code-block:: python

   gv.check_current()

Get the structured analysis object
----------------------------------

Use ``gv.analyze(fig)`` when you want to inspect the returned report object in Python code.

.. code-block:: python

   report = gv.analyze(fig)
