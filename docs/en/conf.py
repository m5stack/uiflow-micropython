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
# import os
import sys

# sys.path.insert(0, os.path.abspath('.'))
import subprocess, os

sys.path.insert(0, os.path.abspath("../../m5stack/libs/"))
# -- Project information -----------------------------------------------------

import datetime

current_year = datetime.datetime.now().year

project = "UIFlow2 Programming Guide"
copyright = "2016 - {} M5Stack Technology Co., Ltd".format(current_year)
author = "pandian"

# The full version, including alpha/beta/rc tags
release = "master"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "breathe",
    "recommonmark",
    "sphinx_markdown_tables",
    "nbsphinx",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.plantuml",
]

autodoc_mock_imports = [
    "micropython",
    "machine",
    "M5",
    "module.mbus",
    "network",
    "m5can",
    "rf433",
    "utime",
    "rui3",
    "m5audio2",
    "lvgl",
    "_espnow",
    "lora"
]

autodoc_default_options = {
    "members": "",
    "show-inheritance": "",
    "member-order": "bysource",
}

autodoc_typehints = "description"
autodoc_docstring_signature = True

# API docs fix
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "micropython": ("https://docs.micropython.org/en/v1.22.0/", None),
    "uiflow2": ("https://uiflow-micropython.readthedocs.io/en/latest/", None),
}

latex_engine = 'pdflatex'

latex_elements = {
    # 这里保留了简单的代码块字体设置，移除了中文排版相关的配置
    'preamble': r'''
\usepackage{listings}
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
}
''',
    'fncychap': '\\usepackage[Bjornstrup]{fncychap}',  # 可选章节样式
    'printindex': r'\footnotesize\raggedright\printindex',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# multi-language docs
language = "en"
locale_dirs = ["../locales/"]
gettext_compact = False  # optional.
gettext_uuid = True  # optional.

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["../_static"]

breathe_projects = {"zbhci": "../build/xml/"}

breathe_default_project = "zbhci"

breathe_domain_by_extension = {
    "h": "c",
    "c": "c",
}

read_the_docs_build = os.environ.get("READTHEDOCS", None) == "True"


if read_the_docs_build:
    subprocess.call("cd ../; doxygen", shell=True)
