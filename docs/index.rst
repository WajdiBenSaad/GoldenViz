GoldenViz documentation
=======================

GoldenViz is a lightweight quality-checking library for Matplotlib charts.
It focuses on 25 Golden Rules of data visualization and is built
for Jupyter notebook workflows as well as explicit manual checks.

Why GoldenViz exists
--------------------

The idea behind GoldenViz comes from teaching data visualization at Universite
Paris Cite. In that setting, one observation became clear: generating a chart
was rarely the main obstacle. With coding assistant tools, examples, and online
documentation, students could usually produce a figure.

The harder part was understanding whether the chart was good, why it needed
corrections, what was misleading or unclear, and what concrete changes would
make it better.

A chart is not finished when it renders. It is finished when a reader can
understand the message quickly, trust the encoding, and spot the important
pattern without unnecessary effort.

Most visualization problems are not syntax problems. They are judgment
problems: missing labels, misleading scales, cluttered legends, too many
categories, unreadable text, inconsistent colors, or visual effects that
distract from the data.

GoldenViz turns those judgment checks into repeatable feedback. It inspects a
figure and reports issues as pass, warning, or fail results, so charts can be
improved before they appear in notebooks, reports, dashboards, papers, or
presentations.

The goal is not to replace the analyst or designer. The goal is to catch common
mistakes early and make good visualization habits easier to apply.

The GoldenViz approach
----------------------

GoldenViz is based on 25 practical rules covering chart purpose, titles, axes,
scales, units, baselines, readability, visual clutter, color, legends, direct
labeling, category handling, uncertainty, precision, dates, diverging values,
and visual economy.

Each rule asks one question: does this chart help the reader understand the
data clearly and honestly?

What makes a good chart?
------------------------

A good chart should:

* have a clear message
* use the right visual encoding for the data
* label what the reader needs to know
* avoid decoration that competes with the signal
* make comparisons easy
* use color deliberately
* show uncertainty or scale when it matters
* respect the reader's time

GoldenViz does not enforce one visual style. It encourages charts that are
readable, honest, and useful.

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   Welcome to GoldenViz! <self>
   installation
   quickstart
   manual_check
   auto_mode
   usage
   examples
   api
   citation_license_trademark
