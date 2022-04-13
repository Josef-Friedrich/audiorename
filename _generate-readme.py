#! /usr/bin/env python


import subprocess
import os
import re
import phrydy
import audiorename


def path(*path_segments):
    return os.path.join(os.getcwd(), *path_segments)


def open_file(*path_segments):
    file_path = path(*path_segments)
    open(file_path, 'w').close()
    return open(file_path, 'a')


template = open(path('README_template.rst'), 'r').read()

process = subprocess.run('audiorenamer --help', capture_output=True,
                         shell=True)
stdout = process.stdout.decode('utf-8')
stdout = '    ' + re.sub(r'\n', '\n    ', stdout)
stdout = phrydy.doc_generator.remove_color(stdout)
template = template.replace('<< cli help >>', stdout)

template = template.replace('<< fields documentation >>',
    phrydy.doc_generator.format_fields_as_rst_table(
        additional_fields=audiorename.fields))

readme = open_file('README.rst')
readme.write(template)
readme.close()

sphinx = open_file('doc', 'source', 'cli.rst')
sphinx_header = (
    'Comande line interface\n',
    '======================\n',
    '\n',
    '.. code-block:: text\n',
    '\n',
)
sphinx.write(''.join(sphinx_header) + stdout)
sphinx.close()
