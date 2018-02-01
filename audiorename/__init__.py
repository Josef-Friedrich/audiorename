# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

from __future__ import print_function

import os
import ansicolor
import phrydy
from .args import parse_args, all_fields
from .batch import Batch
from ._version import get_versions
from collections import namedtuple, OrderedDict
import time
import sys

__version__ = get_versions()['version']
del get_versions


class KeyValue(object):

    def __init__(self, color=False):
        self.color = color
        self.kv = OrderedDict()

    def add(self, key, value):
        self.kv[key] = value

    def result(self):
        out = ''
        for key, value in self.kv.items():
            key = key + ':'
            if self.color:
                key = ansicolor.yellow(key)
            out = out + key + ' ' + value + '\n'
        return out

    def result_one_line(self):
        out = []
        for key, value in self.kv.items():
            if self.color:
                key = ansicolor.green(key)
            out.append(key + '=' + str(value))

        return ' '.join(out)


class Timer(object):

    begin = 0

    end = 0

    def start(self):
        self.begin = time.time()

    def stop(self):
        self.end = time.time()

    def result(self):
        return '{:.1f}s'.format(self.end - self.begin)


class Counter(object):

    def __init__(self):
        self._counters = {}

    def reset(self):
        self._counters = {}

    def count(self, counter):
        """Add one to number identified by a string.

        :param str counter: A string to identify the counter

        :return: None
        """
        if counter in self._counters:
            self._counters[counter] += 1
        else:
            self._counters[counter] = 1

    def get(self, counter):
        """Get the counter identify by a string.

        :param str counter: A string to identify the counter

        :return: The counter as a number
        :rtype: int
        """

        if counter in self._counters:
            return self._counters[counter]
        else:
            return 0

    def result(self):
        out = []
        for counter, value in sorted(self._counters.items()):
            out.append(counter + '=' + str(value))

        if out:
            return ' '.join(out)
        else:
            return 'Nothing to count!'


class Stats(object):

    counter = Counter()
    timer = Timer()


class DefaultFormats(object):

    default = '$ar_initial_artist/' \
              '%shorten{$ar_combined_artist_sort}/' \
              '%shorten{$ar_combined_album}' \
              '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
              '${ar_combined_disctrack}_%shorten{$title}'

    compilation = '_compilations/' \
                  '$ar_initial_album/' \
                  '%shorten{$ar_combined_album}' \
                  '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
                  '${ar_combined_disctrack}_%shorten{$title}'

    soundtrack = '_soundtrack/' \
                 '$ar_initial_album/' \
                 '%shorten{$ar_combined_album}' \
                 '%ifdefnotempty{ar_combined_year,_${ar_combined_year}}/' \
                 '${ar_combined_disctrack}_${artist}_%shorten{$title}'

    classical = '$ar_initial_composer/$ar_combined_composer/' \
                '%shorten{$ar_combined_work_top,48}' \
                '_[%shorten{$ar_classical_performer,32}]/' \
                '${ar_combined_disctrack}_%shorten{$ar_classical_title,64}_' \
                '%shorten{$acoustid_id,8}'


class Formats(object):

    default = u''
    compilation = u''
    soundtrack = u''

    def __init__(self, args):
        defaults = DefaultFormats()

        if args.format:
            defaults.default = args.format

        if args.compilation:
            defaults.compilation = args.compilation

        if args.soundtrack:
            defaults.soundtrack = args.soundtrack

        if args.classical:
            self.default = defaults.classical
            self.compilation = defaults.classical
            self.soundtrack = defaults.classical
        else:
            self.default = defaults.default
            self.compilation = defaults.compilation
            self.soundtrack = defaults.soundtrack


class RenameAction(object):

    def __init__(self, args):
        self._args = args
        self.best_format = args.best_format
        self.backup_folder = args.backup_folder

    @property
    def cleanup(self):
        if self._args.backup:
            return u'backup'
        elif self._args.delete:
            return u'delete'
        else:
            return False

    @property
    def move(self):
        """
        :return:

        :rtype: string

        * copy
        * move
        * no_rename
        """
        if self._args.copy:
            return u'copy'
        elif self._args.move:
            return u'move'
        elif self._args.no_rename:
            return u'no_rename'
        else:
            return u'move'


class Message(object):
    """Print messages on the command line interface.

    :param job: The `job` object
    :type job: audiorename.Job
    """

    def __init__(self, job):
        self.color = job.output.color
        self.verbose = job.output.verbose
        self.one_line = job.output.one_line
        self.max_field = self.max_fields_length()
        self.indent_width = 4

    @staticmethod
    def max_fields_length():
        return phrydy.doc.get_max_field_length(all_fields)

    def output(self, text=''):
        if self.one_line:
            print(text.strip(), end=' ')
        else:
            print(text)

    def template_indent(self, level=1):
        return (' ' * self.indent_width) * level

    def template_path(self, audio_file):
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.short

        if self.color:
            if audio_file.type == 'source':
                path = ansicolor.magenta(path)
            else:
                path = ansicolor.yellow(path)

        return path

    def next_file(self, audio_file):
        print()
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.dir_and_file
        if self.color:
            path = ansicolor.blue(path, reverse=True)
        self.output(path)

    def action_one_path(self, message, audio_file):
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(audio_file))
        self.output()

    def action_two_path(self, message, source, target):
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(source))
        self.output(self.template_indent(2) + 'to:')
        self.output(self.template_indent(2) + self.template_path(target))
        self.output()

    def diff(self, key, value1, value2):
        key_width = self.max_field + 2
        value2_indent = self.indent_width + key_width
        key += ':'
        key = key.ljust(self.max_field + 2)

        def quote(value):
            return '“' + str(value) + '”'

        value1 = quote(value1)
        value2 = quote(value2)
        if self.color:
            value1 = ansicolor.red(value1)
            value2 = ansicolor.green(value2)
            key = ansicolor.yellow(key)
        self.output(self.template_indent(1) + key + value1)
        self.output(' ' * value2_indent + value2)

    def status_color(self, status):
        if status == 'progress':
            return 'yellow'
        elif status == 'error':
            return 'red'
        else:
            return 'green'

    def status(self, text, status):
        if self.color:
            color = getattr(ansicolor, self.status_color(status))
            text = color(text, reverse=True)
        self.output(self.template_indent(1) + text)


class Job(object):
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line.
    This class unifies and processes the data of the `argparse` call. It groups
    the `argparse` key value pairs into parent properties. The properties of
    this class for example can be used to display easily an overview message of
    the job.
    """

    stats = Stats()

    def __init__(self, args):
        self._args = args

        self.field_skip = args.field_skip
        self.shell_friendly = args.shell_friendly
        self.rename = RenameAction(args)
        self.dry_run = args.dry_run
        self.msg = Message(self)

    @property
    def filter(self):
        Filter = namedtuple('Filter', [
            'album_complete',
            'album_min',
            'extension'
        ])

        return Filter(
            self._args.album_complete,
            self._args.album_min,
            self._args.extension.split(',')
        )

    @property
    def format(self):
        """
        default
        compilation
        soundtrack
        """
        return Formats(self._args)

    @property
    def metadata_actions(self):
        MetadataActions = namedtuple('MetadataAction', [
            'enrich_metadata',
            'remap_classical',
        ])

        return MetadataActions(
            self._args.enrich_metadata,
            self._args.remap_classical,
        )
        pass

    @property
    def output(self):
        Output = namedtuple('Output', [
            'color',
            'debug',
            'job_info',
            'mb_track_listing',
            'one_line',
            'stats',
            'verbose',
        ])

        return Output(
            self._args.color,
            self._args.debug,
            self._args.job_info,
            self._args.mb_track_listing,
            self._args.one_line,
            self._args.stats,
            self._args.verbose,
        )

    @property
    def source(self):
        """The source path as a absolute path. Maybe a directory or a file."""
        return os.path.abspath(self._args.source)

    @property
    def target(self):
        """The path of the target path as an absolute path. Is always a
        directory.
        """
        if self._args.source_as_target:
            if os.path.isdir(self.source):
                return os.path.abspath(self.source)
            else:
                return os.path.abspath(os.path.dirname(self.source))
        elif self._args.target:
            return os.path.abspath(self._args.target)
        else:
            return os.getcwd()


def job_info(job):
    import phrydy
    import tmep

    versions = KeyValue(job.output.color)
    versions.add('audiorename', __version__)
    versions.add('phrydy', phrydy.__version__)
    versions.add('tmep', tmep.__version__)

    info = KeyValue(job.output.color)
    info.add('Versions', versions.result_one_line())
    info.add('Action', job.rename.move)
    info.add('Source', job.source)
    info.add('Target', job.target)

    if job.output.verbose:
        info.add('Default', job.format.default)
        info.add('Compilation', job.format.compilation)
        info.add('Soundtrack', job.format.soundtrack)

    print(info.result())


def stats(job):
    kv = KeyValue(job.output.color)

    kv.add('Execution time', job.stats.timer.result())
    kv.add('Counter', job.stats.counter.result())
    print(kv.result())


def execute(*argv):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """

    try:
        args = parse_args(argv)
        job = Job(args)
        job.stats.counter.reset()
        job.stats.timer.start()
        if job.output.job_info:
            job_info(job)
        if job.dry_run:
            job.msg.output('Dry run')
        batch = Batch(job)
        batch.execute()
        job.stats.timer.stop()
        if job.output.stats:
            stats(job)
    except KeyboardInterrupt:
        job.stats.timer.stop()
        if job.output.stats:
            stats(job)
        sys.exit(0)
