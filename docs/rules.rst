Implemented rules
=================

GoldenViz currently implements the first five Golden Rules.

Rule 1. Clear title
-------------------

Checks whether each axis has a title and whether the title is descriptive enough to be useful.

Rule 2. Axis labels
-------------------

Checks whether both axes are labeled. Short labels are accepted but may generate a warning if they are too vague.

Rule 3. Appropriate scale
-------------------------

Checks for obvious scale issues, especially truncated bar charts. Log scales are allowed but flagged so the user can make the choice explicit.

Rule 4. Chart type
------------------

Applies lightweight heuristics to identify line, bar, scatter, and histogram charts and warns when the chosen chart type looks questionable.

Rule 5. Readable labels and ticks
---------------------------------

Checks for overlapping x tick labels, very dense tick marks, and very small tick label font sizes.
