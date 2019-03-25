"""Rename audio files from metadata tags."""

import sys
from .args import parse_args
from .batch import Batch
from .job import Job
from .message import stats, job_info

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


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
