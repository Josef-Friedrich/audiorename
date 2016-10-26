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
        'phrydy',
        'tmep',
        'ansicolor',
        'six',
    ],
    scripts=['bin/audiorenamer'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
    zip_safe=False, )
