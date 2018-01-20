# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
import ansicolor
from .audiofile import Message
from audiorename.args import parse_args
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

        return ' '.join(out)


class Stats(object):

    counter = Counter()
    timer = Timer()


class DefaultFormats(object):

    default = '$artist_initial/' + \
              '%shorten{$artistsafe_sort}/' + \
              '%shorten{$album_clean}%ifdef{year_safe,_${year_safe}}/' + \
              '${disctrack}_%shorten{$title}'

    compilation = '_compilations/' + \
                  '$album_initial/' + \
                  '%shorten{$album_clean}' + \
                  '%ifdef{year_safe,_${year_safe}}/' + \
                  '${disctrack}_%shorten{$title}'

    soundtrack = '_soundtrack/' + \
                 '$album_initial/' + \
                 '%shorten{$album_clean}' + \
                 '%ifdef{year_safe,_${year_safe}}/' + \
                 '${disctrack}_${artist}_%shorten{$title}'

    classical = '$composer_initial/$composer_safe/' + \
                '%shorten{$album_classical,48}' + \
                '_[%shorten{$performer_classical,32}]/' + \
                '${disctrack}_%shorten{$title_classical,64}_' + \
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

    @property
    def cleanup(self):
        if self._args.backup:
            return u'backup'
        elif self._args.delete_existing:
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

    print(info.result())


def stats(job):
    kv = KeyValue(job.output.color)

    kv.add('Execution time', job.stats.timer.result())
    kv.add('Counter', job.stats.counter.result())
    print(kv.result())


def execute(argv=None):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """

    try:
        args = parse_args(argv)
        job = Job(args)
        msg = Message(job)
        job.stats.counter.reset()
        job.stats.timer.start()
        if job.output.job_info:
            job_info(job)
        if job.dry_run:
            msg.output('Dry run')
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
