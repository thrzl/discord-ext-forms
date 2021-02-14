# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../discord'))
sys.path.insert(0, os.path.abspath('../discord/ext'))
sys.path.insert(0, os.path.abspath('../discord/ext/forms'))

# -- Project information -----------------------------------------------------

project = 'discord-ext-forms'
copyright = '2021, Mikey'
author = 'Mikey'

# The full version, including alpha/beta/rc tags
release = '2.6.12'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon','sphinx.ext.viewcode','numpydoc','sphinx.ext.apidoc']#,'sphinx.ext.autodoc','sphinx.ext.autosummary']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
autoapi_dirs = ['../../discord']
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_theme_options = {
    "dark_css_variables":
        {
        "color-brand-primary":'#7289DA',"color-brand-content":'#7289DA'
        },
        "navigation_with_keys":True
    }
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
autosummary_gernerate = True
#autodoc_mock_imports = ['discord']
