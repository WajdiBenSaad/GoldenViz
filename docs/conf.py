import os
import sys
from importlib.metadata import PackageNotFoundError, version as package_version

sys.path.insert(0, os.path.abspath('../src'))

project = 'GoldenViz'
copyright = '2026, Wajdi Ben Saad'
author = 'Wajdi Ben Saad'
try:
    release = package_version('GoldenViz')
except PackageNotFoundError:
    release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', '**.ipynb_checkpoints', 'notebooks/_draft_docs_example_theme.ipynb']
html_theme = 'sphinx_rtd_theme'
html_logo = 'GoldenViz_Logo_transparent.png'
html_static_path = ['_static']
html_css_files = ['goldenviz-theme.css']
nbsphinx_execute = 'never'
autodoc_member_order = 'bysource'
