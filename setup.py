import os

from setuptools import setup, find_packages
import versioneer


def read(file_name):
    """
    Read the contents of a text file and return its content.

    :param str file_name: The name of the file to read.

    :return: The content of the text file.
    :rtype: str
    """
    return open(
        os.path.join(os.path.dirname(__file__), file_name),
        encoding='utf-8'
    ).read()


setup(
    name='audiorename',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Josef Friedrich',
    author_email='josef@friedrich.rocks',
    description=('Rename audio files from metadata tags.'),
    license='MIT',
    packages=find_packages(),
    keywords='audio',
    url='https://github.com/Josef-Friedrich/audiorename',
    install_requires=[
        'phrydy>=1.2.0',
        'tmep>=2.0.0',
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
