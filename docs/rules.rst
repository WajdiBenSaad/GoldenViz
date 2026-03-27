Implemented rules
=================

GoldenViz currently implements the first five Golden Rules.

Rule 1. Clear title
-------------------
Checks whether each axis has a title and whether the title is descriptive enough to be useful.

Rule 2. Axis labels
-------------------
Checks whether both axes are labeled. Short or missing labels may trigger a warning or a failure.

Rule 3. Appropriate scale
-------------------------
Checks for obvious scale issues, especially truncated bar charts.

Rule 4. Chart type
------------------
Applies lightweight heuristics to identify line, bar, scatter, and histogram charts.

Rule 5. Readable labels and ticks
---------------------------------
Checks for dense tick marks, overlapping labels, and hard-to-read axis text.
