.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/audiorename/actions/workflows/test.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/audiorename/actions/workflows/test.yml
    :alt: Tests

.. image:: https://readthedocs.org/projects/audiorename/badge/?version=latest
    :target: https://audiorename.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

***********
audiorename
***********

Rename audio files from metadata tags.

Installation
============

From Github
-----------

.. code:: Shell

    git clone git@github.com:Josef-Friedrich/audiorename.git
    cd audiorename
    python setup.py install

From PyPI
---------

.. code:: Shell

    pip install audiorename
    easy_install audiorename

Examples
========

Please use the ``-d`` (``--dry-run``) option first

Basic example:

.. code:: Shell

    cd my-chaotic-music-collection
    audiorenamer -d .


More advanced example:

.. code:: Shell

    audiorenamer -d -f '$artist/$album/$track $title' --target /mnt/hd/my-organized-music-collection .

Very advanced example:

.. code:: Shell

    audiorenamer -d -f '$ar_initial_artist/%shorten{$ar_combined_artist_sort}/%shorten{$ar_combined_album}%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/${ar_combined_disctrack}_%shorten{$title}' .

Usage
=====

.. code-block:: text

<< cli help >>

Example configuration file
==========================

Use the ``--config`` option to load a configuration file. The command
line arguments overwrite the corresponding options of the configuration
file.

.. code-block:: Shell

    audiorenamer --config /home/user/my-config.ini

Almost all command line arguments have a corresponding option in the
configuration file. ``audiorename`` implements a basic configuration
language which provides a structure similar to what’s found in Microsoft
Windows `INI
<https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_
files:

.. code-block:: ini

<< config file >>

Metadata fields
===============

<< fields documentation >>

Development
===========

Test
----

::

    pyenv local 3.6.13 3.7.10 3.9.2
    pip install tox tox-pyenv
    tox

Run a single test

::

    tox -e quick -- -s test test_job.TestJobWithConfigParser.test_source


Publish a new version
---------------------

::

    git tag 1.1.1
    git push --tags
    python setup.py sdist upload


Package documentation
---------------------

The package documentation is hosted on
`readthedocs <http://audiorename.readthedocs.io>`_.

Generate the package documentation:

::

    python setup.py build_sphinx
