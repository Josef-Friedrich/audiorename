#! /usr/bin/env python


import os
import subprocess

import phrydy

import audiorename
import audiorename.utils


def path(*path_segments: str) -> str:
    return os.path.join(os.getcwd(), *path_segments)


def open_file(*path_segments: str):
    file_path = path(*path_segments)
    open(file_path, "w").close()
    return open(file_path, "a")


template = open(path("README_template.rst"), "r").read()

# cli help
process = subprocess.run("audiorenamer --help", capture_output=True, shell=True)
stdout = process.stdout.decode("utf-8")
print(stdout)
stdout = audiorename.utils.indent(stdout)
stdout = phrydy.doc_generator.remove_color(stdout)
template = template.replace("<< cli help >>", stdout)

# config file
config = open(path("audiorename", "example-config.ini"), "r").read()
config = audiorename.utils.indent(config)
template = template.replace("<< config file >>", config)

# fields documentation
template = template.replace(
    "<< fields documentation >>",
    phrydy.doc_generator.format_fields_as_rst_table(
        additional_fields=audiorename.fields
    ),
)

readme = open_file("README.rst")
readme.write(template)
readme.close()

sphinx = open_file("doc", "source", "cli.rst")
sphinx_header = (
    "Comande line interface\n",
    "======================\n",
    "\n",
    ".. code-block:: text\n",
    "\n",
)
sphinx.write("".join(sphinx_header) + stdout)
sphinx.close()
