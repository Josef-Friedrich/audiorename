"""Helper module for all tests."""

import os
import shutil
import tempfile
import re
import audiorename
import audiorename.meta
import audiorename.audiofile
import musicbrainzngs.musicbrainz
from audiorename import Job
from audiorename.args import ArgsDefault
from audiorename.meta import set_useragent, query_mbrainz
import musicbrainzngs
import subprocess
from jflib import Capturing

SKIP_API_CALLS = False
try:
    set_useragent()
    query_mbrainz('recording', '0480672d-4d88-4824-a06b-917ff408eabe')
except musicbrainzngs.musicbrainz.NetworkError:
    SKIP_API_CALLS = True

dir_cwd = os.getcwd()
path_album = '/t/the album artist/the album_2001/4-02_full.mp3'
path_compilation = '/_compilations/t/the album_2001/4-02_full.mp3'


def get_testfile(*path_list):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files',
                        *path_list)


def get_meta(*path_list):
    return audiorename.meta.Meta(get_testfile(*path_list), False)


def copy_to_tmp(*path_list):
    orig = get_testfile(*path_list)

    tmp = os.path.join(tempfile.mkdtemp(), os.path.basename(orig))
    shutil.copyfile(orig, tmp)
    return tmp


def get_tmp_file_object(*path_list):
    return audiorename.audiofile.AudioFile(copy_to_tmp(*path_list),
                                           job=get_job())


def gen_file_list(files, path, extension='mp3'):
    output = []
    for f in files:
        if extension:
            f = f + '.' + extension
        output.append(os.path.join(path, f))
    return output


def get_job(**arguments):
    args = ArgsDefault()
    for key in arguments:
        setattr(args, key, arguments[key])
    return Job(args)


def has(list, search):
    """Check of a string is in list

    :param list list: A list to search in.
    :param str search: The string to search.
    """
    return any(search in string for string in list)


def is_file(path):
    """Check if file exists

    :param list path: Path of the file as a list
    """
    return os.path.isfile(path)


def join(output_list):
    return ' '.join(output_list)


def dry_run(options):
    """Exectue the audiorename command in the ”dry” mode and capture the
    output to get the renamed file path.

    :param list options: List of additional options

    :return: The renamed file path
    :rtype string:
    """
    with Capturing() as output:
        audiorename.execute(
            '--target', '/',
            '--dry-run',
            '--one-line',
            '--verbose',
            '--shell-friendly', *options)

    return re.sub(r'.* to: ', '', join(output)).strip()


def filter_source(output):
    filtered = []
    for line in output:
        if line and line[0] == os.path.sep:
            filtered.append(line)
    return filtered


def call_bin(*args):
    args = ('audiorenamer',) + args
    command = ' '.join(args)
    audiorename = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    audiorename.wait()
    out = []
    if audiorename.stdout:
        for line in audiorename.stdout.readlines():
            out.append(line.decode('utf-8'))
    return out
