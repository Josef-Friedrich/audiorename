# -*- coding: utf-8 -*-

"""Rename audio files from metadata tags."""

import os
import ansicolor
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

    def count(self, counter):
        setattr(self, counter, getattr(self, counter) + 1)

    def get_counters(self):
        counters = []
        for attr, value in self.__class__.__dict__.items():
            if value == 0:
                counters.append(attr)
        counters.sort()
        return counters

    def result(self):
        counters = self.get_counters()
        out = []
        for counter in counters:
            out.append(counter + '=' + str(getattr(self, counter)))

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

        self.delete_existing = args.delete_existing
        self.field_skip = args.field_skip
        self.shell_friendly = args.shell_friendly

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
    def rename_action(self):
        """
        :return:

        :rtype: string

        * copy
        * dry_run
        * move
        * no_rename
        """
        if self._args.copy:
            return u'copy'
        elif self._args.dry_run:
            return u'dry_run'
        elif self._args.move:
            return u'move'
        elif self._args.no_rename:
            return u'no_rename'
        else:
            return u'move'

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
    info.add('Action', job.rename_action)
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
        job.stats.counter.reset()
        job.stats.timer.start()
        if job.output.job_info:
            job_info(job)
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
