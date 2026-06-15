# GoldenViz

GoldenViz is a lightweight Python library for checking Matplotlib charts
against practical data visualization rules.

It is designed as a visual QA and teaching layer. GoldenViz does not create
charts for you; it inspects charts you already made and returns structured
feedback.

GoldenViz is inspired by the course
[The 25 Golden Rules of Data Viz](https://www.goldenviz.org).

## Installation

```bash
pip install GoldenViz
```

Then import the package with the same capitalization:

```python
import GoldenViz as gv
```

## Quickstart

```python
import matplotlib.pyplot as plt
import GoldenViz as gv

fig, ax = plt.subplots()
ax.plot([2021, 2022, 2023], [10, 14, 13])
ax.set_title("Revenue trend by year")
ax.set_xlabel("Year")
ax.set_ylabel("Revenue (EUR)")

gv.check(fig)
```

To get a structured report instead of displaying it:

```python
report = gv.analyze(fig)
print(report.summary_counts)
```

## Notebook auto mode

```python
import GoldenViz as gv

gv.auto()
```

When auto mode is enabled, GoldenViz tries to show a report after Matplotlib
figures are rendered in notebook workflows.

## Documentation

Full installation, usage, examples, API, citation, license, and trademark
information are available in the documentation:

https://goldenviz.readthedocs.io

## Project status

GoldenViz is currently an alpha package. The implementation is
Matplotlib-first, with Seaborn charts supported when they produce standard
Matplotlib axes.

GoldenViz uses heuristic checks. It can help detect common chart quality
issues, but it does not replace human judgment and may produce false positives
or false negatives.

## Development

From a local checkout:

```bash
pip install -e .
```

For documentation work:

```bash
pip install -e ".[docs]"
```

For tests:

```bash
pip install -e ".[test]"
pytest
```

## License

GoldenViz is free and open source software licensed under the GNU Affero General
Public License version 3 or later (`AGPL-3.0-or-later`). See [LICENSE](LICENSE).

Commercial licensing, enterprise use cases, hosted services, or integrations
that require terms different from AGPLv3 may be available by separate written
agreement.

GoldenViz and the GoldenViz logo are trademarks or claimed trademarks of Wajdi
Ben Saad. Use of the code under AGPLv3 does not grant permission to use the
GoldenViz name or logo to imply endorsement, official status, or partnership.
See [TRADEMARKS.md](TRADEMARKS.md).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
development workflow and contribution licensing terms.
