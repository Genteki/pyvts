import os
import sys
sys.path.insert(0, os.path.abspath(".."))
import pyvts

project = 'pyvts'
copyright = '2023, Genteki'
author = 'Genteki'
release = pyvts.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
]
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '*/tests/*', 'tests/*']
autodoc_typehints = 'description'

html_theme_options = {
    'navigation_depth': 3,
}

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
