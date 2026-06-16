# GoldenViz

GoldenViz is a lightweight Python library for checking Matplotlib charts
against practical data visualization rules.

It is designed as a visual QA and teaching layer. GoldenViz does not create
charts for you; it inspects charts you already made and returns structured
feedback.

GoldenViz is inspired by the course and book:
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
ax.plot([2021, 2022, 2023], [10, 13, 16])
ax.set_title("Revenue trend by year")
ax.set_xlabel("Year")
ax.set_ylabel("Revenue (M EUR)")

gv.check(fig)
```

Running the code displays the Matplotlib chart first, then a GoldenViz report.
The report summarizes the checks and lists the rules that need attention:

```text
GoldenViz report
Automatic visual QA for the 25 Golden Rules.

PASS 25 | WARNING 0 | FAIL 0

Axis: Revenue trend by year
Needs attention: none

Passing checks include:
- Clear title: PASS
- Axis labels: PASS
- Units and scale clarity: PASS
```

The documentation includes the rendered chart and full HTML report preview:
https://goldenviz.readthedocs.io/en/latest/installation.html

Report preview:

![GoldenViz report preview](https://raw.githubusercontent.com/WajdiBenSaad/GoldenViz/main/docs/_static/goldenviz_installation_check_report.png)

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

See [CHANGELOG.md](CHANGELOG.md) for release notes.

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
