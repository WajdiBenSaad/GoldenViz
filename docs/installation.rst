Installation
============

GoldenViz is available as a Python package. The recommended way to install it
is with ``pip`` in a project-specific virtual environment.

Install from PyPI
-----------------

.. code-block:: bash

   pip install GoldenViz

After installation, import the library with the same capitalization:

.. code-block:: python

   import GoldenViz as gv

Check your installation
-----------------------

Run this small example to confirm that GoldenViz can inspect a Matplotlib
figure:

.. code-block:: python

   import matplotlib.pyplot as plt
   import GoldenViz as gv

   fig, ax = plt.subplots()
   ax.plot([2021, 2022, 2023], [10, 13, 16])
   ax.set_title("Revenue trend by year")
   ax.set_xlabel("Year")
   ax.set_ylabel("Revenue (M EUR)")

   gv.check(fig)

After running the code, you should see two outputs: first the Matplotlib chart,
then the GoldenViz report.

Expected chart output:

.. image:: _static/goldenviz_installation_check_chart.png
   :alt: Matplotlib chart produced by the installation check
   :align: center
   :width: 50%

Expected GoldenViz report output:

.. raw:: html
   :file: _static/goldenviz_installation_check_report.html

Notebook users
--------------

GoldenViz works well in Jupyter notebooks and VS Code notebooks. For the best
notebook experience, make sure ``ipykernel`` is installed in the same
environment:

.. code-block:: bash

   pip install ipykernel

Then enable automatic chart checks inside a notebook:

.. code-block:: python

   import GoldenViz as gv

   gv.auto()

Development install
-------------------

If you are contributing to GoldenViz or working from a local checkout, install
the project in editable mode:

.. code-block:: bash

   pip install -e .

Documentation dependencies:

.. code-block:: bash

   pip install -e ".[docs]"

Test dependencies:

.. code-block:: bash

   pip install -e ".[test]"
