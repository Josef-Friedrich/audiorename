import audiorename

html_theme = "sphinx_rtd_theme"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
source_suffix = ".rst"

master_doc = "index"

project = "audiorename"
copyright = "2016 - 2022, Josef Friedrich"
author = "Josef Friedrich"
version = audiorename.__version__
release = audiorename.__version__
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

autodoc_default_options = {"members": True, "show-inheritance": True}

htmlhelp_basename = "audiorenamedoc"

[extensions]
todo_include_todos = True
