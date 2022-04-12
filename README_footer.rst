
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

    tox -e py38 -- test/test_audiofile.py:TestUnicodeUnittest.test_rename


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
