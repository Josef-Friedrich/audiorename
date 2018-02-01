import versioneer
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='audiorename',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Josef Friedrich',
    author_email='josef@friedrich.rocks',
    description=('Rename audio files from metadata tags.'),
    license='MIT',
    packages=['audiorename'],
    keywords='audio',
    url='https://github.com/Josef-Friedrich/audiorename',
    install_requires=[
        'phrydy>=1.1.9',
        'tmep>=1.0.7',
        'ansicolor',
        'six',
        'musicbrainzngs',
    ],
    scripts=['bin/audiorenamer'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    zip_safe=False, )
