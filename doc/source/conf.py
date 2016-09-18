extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]
templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

project = u'audiorename'
copyright = u'2016, Josef Friedrich'
author = u'Josef Friedrich'
version = u'0.0.5'
release = u'0.0.5'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
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
