# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
import ansicolor
from audiorename.args import parse_args
from .batch import Batch
from ._version import get_versions
from collections import namedtuple
import time

__version__ = get_versions()['version']
del get_versions


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

    exists = 0
    no_field = 0
    rename = 0
    renamed = 0
    dry_run = 0

    def reset(self):
        self.exists = 0
        self.no_field = 0
        self.rename = 0
        self.renamed = 0
        self.dry_run = 0


class Stats(object):

    counter = Counter()


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


class Job(object):
    """Holds informations of one job which can handle multiple files.

    A jobs represents one call of the program on the command line.
    This class unifies and processes the data of the `argparse` call. It groups
    the `argparse` key value pairs into parent properties. The properties of
    this class for example can be used to display easily an overview message of
    the job.
    """

    stats = Stats()

    timer = Timer()

    def __init__(self, args):
        self._args = args

        self.delete_existing = args.delete_existing
        self.skip_if_empty = args.skip_if_empty
        self.shell_friendly = args.shell_friendly

    @property
    def action(self):
        """
        :return:

        :rtype: string

        * copy
        * dry_run
        * mb_track_listing
        * move
        * work

        """
        if self._args.copy:
            return u'copy'
        elif self._args.dry_run:
            return u'dry_run'
        elif self._args.mb_track_listing:
            return u'mb_track_listing'
        elif self._args.move:
            return u'move'
        elif self._args.work:
            return u'work'
        else:
            return u'move'

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
            self._args.extension
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
    def output(self):
        Output = namedtuple('Output', [
            'color',
            'job_info',
            'one_line',
            'stats',
            'verbose',
        ])

        return Output(
            self._args.color,
            self._args.job_info,
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


class MessageJob(object):

    def __init__(self, job):
        self.job = job
        self.job_properties = ['action', 'source', 'target']

    def format_key_value(self, key, value):
        key = key + ':'
        if self.job.output.color:
            key = ansicolor.yellow(key)
        return key + ' ' + value + '\n'

    def versions(self):
        import phrydy
        import tmep
        return self.format_key_value('audiorename', __version__) + \
            self.format_key_value('phrydy', phrydy.__version__) + \
            self.format_key_value('tmep', tmep.__version__)

    def print_output(self):
        out = self.versions()
        for prop in self.job_properties:
            out = out + self.format_key_value(prop, getattr(self.job, prop))

        print(out)


def print_stats(job):
    if job.output.stats:
        print(job.timer.result())
        print(job.stats.counter.rename)
        print(job.stats.counter.dry_run)


def execute(argv=None):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """
    args = parse_args(argv)
    job = Job(args)
    job.stats.counter.reset()
    job.timer.start()
    if job.output.job_info:
        message = MessageJob(job)
        message.print_output()
    batch = Batch(job)
    batch.execute()
    job.timer.stop()
    print_stats(job)
