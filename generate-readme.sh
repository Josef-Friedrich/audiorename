#! /bin/sh

cat <<EOF
Install the latest versions of the packages “audiorename”, “phrydy”
and “tmep” to get an up-to-date README file.

Using pip:

        pip install --upgrade audiorename

        pip install --upgrade phrydy
        pip install --upgrade tmep

Using the git repos:

        cd audiorename; python setup.py develop

        cd phrydy; python setup.py develop
        cd tmep; python setup.py develop

EOF

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
