API reference
=============

This page documents the public GoldenViz API. Most users only need three
functions:

- ``gv.check(fig)`` to analyze and display a report for a specific figure.
- ``gv.check_current()`` to analyze the current active Matplotlib figure.
- ``gv.analyze(fig)`` to get structured Python results without displaying a report.

GoldenViz works with Matplotlib figures. Seaborn charts are supported when they
produce standard Matplotlib figures and axes.


Import convention
-----------------

Install the package as ``GoldenViz`` and import it with the same capitalization:

.. code-block:: python

   import GoldenViz as gv


Manual analysis
---------------

Use manual analysis when you want explicit control over which figure GoldenViz
checks.

``analyze(fig=None)``
~~~~~~~~~~~~~~~~~~~~~

Analyze a Matplotlib figure and return a structured report object.

Use this when you want to inspect results in Python code, write tests, build a
custom report, or integrate GoldenViz into another workflow.

.. code-block:: python

   import matplotlib.pyplot as plt
   import GoldenViz as gv

   fig, ax = plt.subplots()
   ax.plot([2021, 2022, 2023], [10, 14, 13])
   ax.set_title("Revenue trend by year")
   ax.set_xlabel("Year")
   ax.set_ylabel("Revenue (M EUR)")

   report = gv.analyze(fig)

   print(report.summary_counts)
   print(len(report.rule_results))

When ``fig`` is omitted, GoldenViz analyzes the current active Matplotlib
figure.

.. autofunction:: GoldenViz.analyze


``check(fig=None, display=True)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyze a figure and optionally display the GoldenViz report.

Use this as the main interactive API when you already have a ``fig`` object.
With the default ``display=True``, GoldenViz displays a report and returns
``None``. With ``display=False``, it returns the same structured
``FigureReport`` object as ``analyze``.

.. code-block:: python

   gv.check(fig)

.. code-block:: python

   report = gv.check(fig, display=False)

.. autofunction:: GoldenViz.check


``check_current(display=True)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyze the current active Matplotlib figure.

This is convenient in notebooks or scripts where you just created one chart and
do not want to keep a separate ``fig`` variable. For larger notebooks or
multi-figure workflows, ``check(fig)`` is usually clearer because it makes the
target figure explicit.

.. code-block:: python

   import matplotlib.pyplot as plt
   import GoldenViz as gv

   plt.plot([2021, 2022, 2023], [10, 14, 13])
   plt.title("Revenue trend by year")
   plt.xlabel("Year")
   plt.ylabel("Revenue (M EUR)")

   gv.check_current()

.. autofunction:: GoldenViz.check_current


Notebook automatic mode
-----------------------

Automatic mode is designed for notebook workflows. After it is enabled,
GoldenViz tries to append a report below Matplotlib figures as they render.

``auto()``
~~~~~~~~~~

Enable automatic report display for future Matplotlib figures.

.. code-block:: python

   import GoldenViz as gv

   gv.auto()

.. autofunction:: GoldenViz.auto


``disable()``
~~~~~~~~~~~~~

Disable automatic mode and restore Matplotlib display behavior.

.. code-block:: python

   gv.disable()

.. autofunction:: GoldenViz.disable


``is_auto_enabled()``
~~~~~~~~~~~~~~~~~~~~~

Return whether automatic mode is currently active.

.. code-block:: python

   if gv.is_auto_enabled():
       print("GoldenViz auto mode is active")

.. autofunction:: GoldenViz.is_auto_enabled


Report objects
--------------

GoldenViz separates analysis from display. The analyzer returns structured
dataclasses that can be inspected directly, rendered as HTML, rendered as text,
or used in tests.


``FigureReport``
~~~~~~~~~~~~~~~~

Top-level report returned for one Matplotlib figure.

Important attributes and properties:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Meaning
   * - ``figure_number``
     - Matplotlib figure number when available.
   * - ``axes_reports``
     - List of ``AxisReport`` objects, one for each visible axis.
   * - ``rendered_in_notebook``
     - Whether the report was displayed through the notebook HTML path.
   * - ``rule_results``
     - Flat list of all ``RuleResult`` objects across all visible axes.
   * - ``summary_counts``
     - Dictionary counting ``PASS``, ``WARNING``, ``FAIL``, and ``INFO`` results.

.. autoclass:: GoldenViz._results.FigureReport
   :members:


``AxisReport``
~~~~~~~~~~~~~~

Report for one visible Matplotlib axis.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Meaning
   * - ``axis_index``
     - Zero-based position of the visible axis inside the analyzed figure.
   * - ``axis_title``
     - Axis title when available.
   * - ``rule_results``
     - Ordered list of ``RuleResult`` objects for the 25 GoldenViz rules.

.. autoclass:: GoldenViz._results.AxisReport
   :members:


``RuleResult``
~~~~~~~~~~~~~~

Result for one rule applied to one axis.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Attribute
     - Meaning
   * - ``rule_id``
     - Stable rule identifier such as ``R1``.
   * - ``rule_name``
     - Human-readable rule name shown in reports.
   * - ``status``
     - Rule status: ``PASS``, ``WARNING``, ``FAIL``, or ``INFO``.
   * - ``message``
     - Main assessment message.
   * - ``suggestion``
     - Optional repair or improvement suggestion.
   * - ``axis_title``
     - Axis title associated with the result, when available.
   * - ``details``
     - Extra structured information for debugging or future integrations.

.. autoclass:: GoldenViz._results.RuleResult
   :members:


Status values
-------------

GoldenViz rule results use four status labels.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status
     - Meaning
   * - ``PASS``
     - The rule did not detect a problem for the inspected axis.
   * - ``WARNING``
     - The chart may need attention, but the issue depends on context.
   * - ``FAIL``
     - The rule detected a stronger problem that should usually be fixed.
   * - ``INFO``
     - Informational result reserved for non-blocking context.


Working with reports
--------------------

You can inspect the report object directly:

.. code-block:: python

   report = gv.analyze(fig)

   for axis_report in report.axes_reports:
       print(axis_report.axis_title)
       for result in axis_report.rule_results:
           if result.status != "PASS":
               print(result.rule_id, result.rule_name, result.status)
               print(result.message)
               if result.suggestion:
                   print("Suggestion:", result.suggestion)

You can also use ``summary_counts`` for a compact overview:

.. code-block:: python

   counts = report.summary_counts

   if counts["FAIL"] or counts["WARNING"]:
       print("This chart needs attention.")


Version
-------

GoldenViz exposes its package version as ``__version__``.

.. code-block:: python

   import GoldenViz as gv

   print(gv.__version__)

