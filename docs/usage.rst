Usage
=====

Here is a basic example of how to use **GoldenViz** to analyze a matplotlib figure and check if it follows the Golden Rules of Data Visualization.

.. code-block:: python

   import matplotlib.pyplot as plt
   from GoldenViz import visualize_rules  # Assuming this will be your module later

   # Create a simple figure
   fig, ax = plt.subplots()
   ax.plot([1, 2, 3], [10, 20, 15])
   ax.set_title("Sample Plot")

   # Analyze the figure with GoldenViz
   # This will output potential issues and recommendations based on the Golden Rules
   # visualize_rules.check_figure(fig)
