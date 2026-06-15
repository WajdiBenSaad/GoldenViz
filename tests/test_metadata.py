import re
from pathlib import Path

import GoldenViz as gv


ROOT = Path(__file__).resolve().parents[1]


def _quoted_value(text, key):
    match = re.search(rf'^{re.escape(key)}:\s*"([^"]+)"\s*$', text, re.MULTILINE)
    assert match is not None, f"{key} not found"
    return match.group(1)


def test_package_version_matches_pyproject():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"\s*$', pyproject, re.MULTILINE)

    assert match is not None
    assert gv.__version__ == match.group(1)


def test_citation_version_matches_package_version():
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")

    assert _quoted_value(citation, "version") == gv.__version__
