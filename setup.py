import os

from setuptools import setup, find_packages
import versioneer


def read(file_name: str) -> str:
    """
    Read the contents of a text file and return its content.

    :param file_name: The name of the file to read.

    :return: The content of the text file.
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
        'phrydy==3.0.1',
        'tmep==2.0.2',
        'ansicolor==0.3.2',
        'musicbrainzngs==0.7.1',
    ],
    scripts=['bin/audiorenamer'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    zip_safe=False,
    include_package_data=True,
    package_data={
        '': ['*.ini'],

    },
)
