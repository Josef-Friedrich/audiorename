import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='audiorename',
    version='0.0.5',
    author='Josef Friedrich',
    author_email='josef@friedrich.rocks',
    description=('Rename audio files from metadata tags.'),
    license='MIT',
    packages=['audiorename'],
    keywords='audio',
    url='https://github.com/Josef-Friedrich/audiorename',
    install_requires=[
        'phrydy',
        'tmep',
        'ansicolor',
        'six',
    ],
    scripts=['bin/audiorenamer'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    zip_safe=False, )
