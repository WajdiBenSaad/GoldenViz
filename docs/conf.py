import os
import sys

sys.path.insert(0, os.path.abspath('../src'))

project = 'GoldenViz'
copyright = '2026, Wajdi Ben Saad'
author = 'Wajdi Ben Saad'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', '**.ipynb_checkpoints']
html_theme = 'sphinx_rtd_theme'
nbsphinx_execute = 'never'
autodoc_member_order = 'bysource'
