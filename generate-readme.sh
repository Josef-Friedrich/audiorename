#! /bin/sh

echo '.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename


.. code-block:: text

' > README.rst

./bin/audiorenamer -h | sed 's/^/    /g' >> README.rst


echo 'Comande line interface
======================

.. code-block:: text

' > doc/source/cli.rst

./bin/audiorenamer -h | sed 's/^/    /g' >> doc/source/cli.rst
