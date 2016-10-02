import sphinx_rtd_theme
import audiorename

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

project = u'audiorename'
copyright = u'2016, Josef Friedrich'
author = u'Josef Friedrich'
version = audiorename.__version__
release = audiorename.__version__
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_static_path = []
htmlhelp_basename = 'audiorenamedoc'

latex_elements = {
     'papersize': 'a4paper',
     'pointsize': '11pt',
}

latex_documents = [
    (master_doc, 'audiorename.tex', u'audiorename Documentation',
     u'Josef Friedrich', 'manual'),
]

man_pages = [
    (master_doc, 'audiorename', u'audiorename Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'audiorename', u'audiorename Documentation',
     author, 'audiorename', 'Rename audio files from metadata tags.',
     'Miscellaneous'),
]
