#! /bin/sh

cat README_header.rst > README.rst
echo >> README.rst
./bin/audiorenamer -h | sed 's/^/    /g' >> README.rst
echo >> README.rst
cat README_footer.rst >> README.rst

echo 'Comande line interface
======================

.. code-block:: text

' > doc/source/cli.rst

./bin/audiorenamer -h | sed 's/^/    /g' >> doc/source/cli.rst
