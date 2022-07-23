"""Rename audio files from metadata tags."""

import sys
from importlib import metadata

from .args import fields, parse_args
from .batch import Batch
from .job import Job
from .message import job_info, stats

fields

__version__: str = metadata.version("audiorename")


def execute(*argv: str):
    """Main function

    :param list argv: The command line arguments specified as a list: e. g
        :code:`['--dry-run', '.']`
    """

    job = None

    try:
        args = parse_args(argv)
        job = Job(args)
        job.stats.counter.reset()
        job.stats.timer.start()
        if job.cli_output.job_info:
            job_info(job)
        if job.rename.dry_run:
            job.msg.output("Dry run")
        batch = Batch(job)
        batch.execute()
        job.stats.timer.stop()
        if job.cli_output.stats:
            stats(job)
    except KeyboardInterrupt:
        if job:
            job.stats.timer.stop()
            if job.cli_output.stats:
                stats(job)
        sys.exit(0)
