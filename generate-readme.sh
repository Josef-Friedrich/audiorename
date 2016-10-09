#! /bin/sh

echo '.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename


.. code-block:: none
' > README.rst

./bin/audiorenamer -h | sed 's/^/  /g' >> README.rst
