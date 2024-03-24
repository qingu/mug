# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser
project = 'mcv-notes'
copyright = '2024, MetMan'
author = 'MetMan'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# html_theme = 'alabaster'
# html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

source_parsers = {
    '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']
extensions = ['recommonmark', 'sphinx_markdown_tables']
