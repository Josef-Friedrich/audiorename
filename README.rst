.. image:: http://img.shields.io/pypi/v/audiorename.svg
    :target: https://pypi.python.org/pypi/audiorename

.. image:: https://travis-ci.org/Josef-Friedrich/audiorename.svg?branch=packaging
    :target: https://travis-ci.org/Josef-Friedrich/audiorename


usage: audiorenamer [-h] [-f FORMAT] [-c COMPILATION] [-S] [-d]
                    [-e EXTENSIONS] [-t TARGET_DIR] [-s SKIP_IF_EMPTY] [-a]
                    [-C]
                    folder

Rename audio files from metadata tags.

How to specify the target directory?

1. By the default the audio files are moved or renamed to the parent
   working directory.
2. Use the option ``-t <folder>`` or ``--target-dir <folder>`` to specifiy
   a target directory.
3. Use the option ``-a`` or ``--source-as-target-dir`` to copy or rename
   your audio files within the source directory.

positional arguments:
  folder                A folder containing audio files or a audio file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        A format string
  -c COMPILATION, --compilation COMPILATION
                        Format string for compilations
  -S, --shell-friendly  Rename audio files “shell friendly”, this means
                        without whitespaces, parentheses etc.
  -d, --dry-run         Don’t rename or copy the audio files.
  -e EXTENSIONS, --extensions EXTENSIONS
                        Extensions to rename
  -t TARGET_DIR, --target-dir TARGET_DIR
                        Target directory
  -s SKIP_IF_EMPTY, --skip-if-empty SKIP_IF_EMPTY
                        Skip renaming of field is empty.
  -a, --source-as-target-dir
                        Use specified source folder as target directory
  -C, --copy            Copy files instead of rename / move.
