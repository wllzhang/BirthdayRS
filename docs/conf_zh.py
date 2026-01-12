# Chinese configuration for BirthdayRS documentation
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'BirthdayRS'
copyright = '2026, BirthdayRS 贡献者'
author = 'BirthdayRS 贡献者'
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
language = 'zh_CN'
locale_dirs = ['locale/']
gettext_compact = False
gettext_uuid = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']

# Furo theme customization
html_title = 'BirthdayRS 文档'
html_logo = '_static/logo.svg'
html_theme_options = {
    'sidebar_hide_name': False,
    'navigation_with_keys': True,
    'source_repository': 'https://github.com/wllzhang/BirthdayRS',
    'source_branch': 'main',
    'source_directory': 'docs/',
    'top_of_page_buttons': [],
    'announcement': '文档从源代码自动生成',
}

# Language selector
html_context = {
    'display_github': True,
    'github_user': 'wllzhang',
    'github_repo': 'BirthdayRS',
    'github_version': 'main/docs/',
    'conf_py_path': '/docs/',
    'current_language': 'zh',
    'languages': [('en', 'English'), ('zh', '中文')],
    'links': {'en': '../'},
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
