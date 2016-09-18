extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]
templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

project = u'tmep'
copyright = u'2016, Josef Friedrich'
author = u'Josef Friedrich'
version = u'0.0.3'
release = u'0.0.3'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'tmepdoc'

latex_elements = {
     'papersize': 'a4paper',
     'pointsize': '11pt',
}

latex_documents = [
    (master_doc, 'tmep.tex', u'tmep Documentation',
     u'Josef Friedrich', 'manual'),
]

man_pages = [
    (master_doc, 'tmep', u'tmep Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'tmep', u'tmep Documentation',
     author, 'tmep', 'One line description of project.',
     'Miscellaneous'),
]

