# Minimal Sphinx configuration for BirthdayRS documentation
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'BirthdayRS'
copyright = '2026, BirthdayRS Contributors'
author = 'BirthdayRS Contributors'
release = '0.1.0'
version = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Internationalization ----------------------------------------------------
language = 'en'

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']

# Furo theme customization
html_title = 'BirthdayRS Documentation'
html_logo = '_static/logo.svg'
html_theme_options = {
    'sidebar_hide_name': False,
    'navigation_with_keys': True,
    'source_repository': 'https://github.com/wllzhang/BirthdayRS',
    'source_branch': 'main',
    'source_directory': 'docs/',
    'top_of_page_buttons': [],
    'announcement': 'Documentation auto-generated from source code',
}

# Language selector
html_context = {
    'display_github': True,
    'github_user': 'wllzhang',
    'github_repo': 'BirthdayRS',
    'github_version': 'main/docs/',
    'conf_py_path': '/docs/',
    'current_language': 'en',
    'languages': [('en', 'English'), ('zh', '中文')],
    'links': {'zh': 'zh/'},
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'click': ('https://click.palletsprojects.com/', None),
}

# -- Autosummary configuration ------------------------------------------------
autosummary_generate = True

# -- Todo extension -----------------------------------------------------------
todo_include_todos = True

# -- Master document ----------------------------------------------------------
master_doc = 'index'
