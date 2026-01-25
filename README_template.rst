{{ badge.pypi }}

{{ badge.github_workflow() }}

{{ badge.readthedocs }}

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

{{ cli('audiorenamer --help') | literal }}

Configuration files
===================

Use the ``--config`` option to load a configuration file. The command
line arguments overwrite the corresponding options of the configuration
file.

.. code-block:: Shell

    audiorenamer --config /home/user/my-config.ini

It is also possible to load several configuration files. Values of the
latter file overwrite the values of the first files.

.. code-block:: Shell

    audiorenamer --config base.ini --config overload.ini

Almost all command line arguments have a corresponding option in the
configuration file. ``audiorename`` implements a basic configuration
language which provides a structure similar to what’s found in Microsoft
Windows `INI
<https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_
files:

{{ read('src/audiorename/example-config.ini') | code('ini') }}

Metadata fields
===============

{{ func('audiorename.args.format_fields_as_rst_table') }}
