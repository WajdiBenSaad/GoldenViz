# Contributing To GoldenViz

Thanks for considering a contribution to GoldenViz.

GoldenViz is currently an alpha-stage project. Contributions are welcome, but
the project is still shaping its API, rule set, documentation, and release
process.

## AI-Assisted Contributions

AI coding assistants may be used, but the human contributor is fully
responsible for the contribution.

If AI generated or materially shaped a substantial part of the code, tests,
documentation, examples, or pull request text, disclose that in the pull request
description and briefly state:

- which tool was used
- which parts were AI-assisted
- how the result was reviewed and tested

Do not submit code you do not understand. Do not submit AI-generated output that
may reproduce third-party copyrighted code or introduce license conflicts.

Maintainers may reject AI-assisted contributions that are untested, unclear,
overly broad, unverifiable, or difficult to review.

## Before You Start

For non-trivial changes, please open an issue first. This helps avoid duplicate
work and keeps the project direction coherent.

Good first contributions include:

- bug reports with small reproducible examples
- documentation fixes
- focused test cases
- small rule-quality improvements
- examples that clarify existing behavior

Larger features, new rule families, API changes, or report-format changes
should be discussed before implementation.

## Development Setup

Install the package locally:

```bash
pip install -e ".[test,docs]"
```

Run the tests:

```bash
python -m pytest
```

Build the documentation:

```bash
cd docs
make html
```

## Pull Request Expectations

Pull requests should be:

- focused on one change
- covered by tests when behavior changes
- documented when user-facing behavior changes
- consistent with the existing code style
- linked to an issue when the change is non-trivial

## Licensing Of Contributions

GoldenViz is licensed under the GNU Affero General Public License version 3 or
later (`AGPL-3.0-or-later`).

By submitting a contribution, you agree that your contribution is licensed under
the same license as the project unless explicitly agreed otherwise in writing.

For larger contributions, substantial new modules, or work that may affect
future commercial licensing options, the maintainer may require a separate
contributor agreement before accepting the contribution.

## Trademarks

The GoldenViz name and logo are governed by the project trademark policy in
`TRADEMARKS.md`. The code license does not grant permission to use the
GoldenViz name or logo to imply endorsement, official status, or partnership.
