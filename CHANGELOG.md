# Changelog

## 0.1.0 - 2026-06-16

### Changed

- Promoted the alpha release line to the first stable PyPI-visible `0.1.0` release.
- Keeps the release infrastructure fixes and README visual preview from `0.1.0a2`.
- Simplified the README report preview so it renders cleanly on PyPI.

## 0.1.0a2 - 2026-06-16

### Fixed

- Added Pandoc setup for GitHub Actions and ReadTheDocs documentation builds.
- Updated GitHub workflow actions to Node 24-compatible versions.

### Changed

- Added a README visual preview showing the Matplotlib quickstart chart and a compact GoldenViz HTML report.

## 0.1.0a1 - 2026-06-16

### Added

- Initial alpha release of GoldenViz.
- Analysis of Matplotlib figures against the 25 Golden Rules of data visualization.
- Manual checks with `gv.check()`, `gv.check_current()`, and `gv.analyze()`.
- Notebook automatic mode with `gv.auto()`.
- Structured report objects for programmatic use.
- HTML and text report renderers.
- Documentation pages for installation, quick start, manual checks, auto mode, examples, citation, license, and trademark information.
- Expanded API reference covering public functions, report objects, status values, and programmatic usage patterns.
- Example gallery covering the 25 rules.
- CI checks for tests, documentation build, package build, metadata validation, and clean wheel install smoke testing.

### Changed

- Reordered the 25 rules into Completeness, Readability, and Integrity families.
- Updated documentation examples and report output to match the current GoldenViz report layout.

### Known limitations

- GoldenViz is currently an alpha release; rule checks are heuristic and may produce false positives or false negatives.
- The current test suite covers the public API, report generation, metadata, packaging, and selected rule behavior, but not every edge case for all 25 rules.
- Notebook execution and visual regression testing are not yet part of CI.
