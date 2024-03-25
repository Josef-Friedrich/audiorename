"""Helper module for all tests."""

import os
import re
import shutil
import subprocess
import tempfile
import typing

import musicbrainzngs
import musicbrainzngs.musicbrainz
from stdout_stderr_capturing import Capturing

import audiorename
import audiorename.audiofile
import audiorename.meta
from audiorename import Job
from audiorename.args import ArgsDefault
from audiorename.musicbrainz import query, set_useragent

SKIP_API_CALLS = False
try:
    set_useragent()
    query("recording", "0480672d-4d88-4824-a06b-917ff408eabe")
except musicbrainzngs.musicbrainz.NetworkError:
    SKIP_API_CALLS = True

SKIP_QUICK = "QUICK" in os.environ

dir_cwd = os.getcwd()
path_album = "/t/the album artist/the album_2001/4-02_full.mp3"
path_compilation = "/_compilations/t/the album_2001/4-02_full.mp3"


def get_testfile(*path_list: str) -> str:
    """
    Get absolute path of a test file.

    :param path_list: Path segments relative to the /tests/files directory.

    :return An absolute path:
    """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", *path_list)


def get_meta(*path_list: str) -> audiorename.meta.Meta:
    return audiorename.meta.Meta(get_testfile(*path_list), False)


def copy_to_tmp(*path_list: str) -> str:
    orig = get_testfile(*path_list)

    tmp = os.path.join(tempfile.mkdtemp(), os.path.basename(orig))
    shutil.copyfile(orig, tmp)
    return tmp


def get_tmp_file_object(*path_list: str):
    return audiorename.audiofile.AudioFile(copy_to_tmp(*path_list), job=get_job())


def gen_file_list(
    files: typing.List[str], path: str, extension: str = "mp3"
) -> typing.List[str]:
    output: typing.List[str] = []
    for f in files:
        if extension:
            f = f + "." + extension
        output.append(os.path.join(path, f))
    return output


def get_job(**arguments: str) -> Job:
    args = ArgsDefault()
    for key in arguments:
        setattr(args, key, arguments[key])
    return Job(args)


def has(list: typing.List[str], search: str) -> bool:
    """Check of a string is in list

    :param list list: A list to search in.
    :param str search: The string to search.
    """
    return any(search in string for string in list)


def is_file(path: str) -> bool:
    """Check if file exists

    :param list path: Path of the file as a list
    """
    return os.path.isfile(path)


def join(output_list: typing.List[str]) -> str:
    return " ".join(output_list)


def dry_run(options: typing.List[str]):
    """Exectue the audiorename command in the ”dry” mode and capture the
    output to get the renamed file path.

    :param list options: List of additional options

    :return: The renamed file path
    :rtype string:
    """
    with Capturing() as output:
        audiorename.execute(
            "--target",
            "/",
            "--dry-run",
            "--one-line",
            "--verbose",
            "--shell-friendly",
            *options,
        )

    return re.sub(r".* to: ", "", join(output)).strip()


def filter_source(output: typing.List[str]) -> typing.List[str]:
    filtered: typing.List[str] = []
    for line in output:
        if line and line[0] == os.path.sep:
            filtered.append(line)
    return filtered


def call_bin(*args: str) -> typing.List[str]:
    args = ("audiorenamer",) + args
    command = " ".join(args)
    audiorename = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    audiorename.wait()
    out: typing.List[str] = []
    if audiorename.stdout:
        for line in audiorename.stdout.readlines():
            out.append(line.decode("utf-8"))
    return out
