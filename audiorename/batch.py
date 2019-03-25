"""Batch processing of the audio files."""

from audiorename.audiofile import do_job_on_audiofile
from audiorename.audiofile import mb_track_listing
from phrydy import MediaFile
import os
import phrydy


class Batch(object):
    """This class first sorts all files and then walks through all files. At
    this process it tries to make bundles of files belonging to a album. This
    bundle of files is temporary stores in the attribute `virtual_album`. This
    complicated mechanism is needed for the both filters `album_complete` and
    `album_min`.

    :param job: The `job` object.
    :type job: audiorename.job.Job
    """

    virtual_album = []
    """Storage of a list of files belonging to an album."""

    current_album_title = ''
    """Storage for the album title of the current audio file."""

    def __init__(self, job):
        self.job = job
        self.bundle_filter = job.filter.album_complete or job.filter.album_min

    def check_extension(self, path):
        """Check the extension of the track.

        :params str path: The path of the tracks.
        """
        extension = self.job.filter.extension
        extension = ['.' + e for e in extension]
        if path.lower().endswith(tuple(extension)):
            return True
        else:
            return False

    def check_quantity(self):
        """Compare the number of tracks in an album with the minimal track
        threshold.
        """
        if len(self.virtual_album) > int(self.job.filter.album_min):
            return True
        else:
            return False

    def check_completeness(self):
        """Check if the album is complete"""
        max_track = 0
        for record in self.virtual_album:
            if record['track'] > max_track:
                max_track = record['track']

        if len(self.virtual_album) == max_track:
            return True
        else:
            return False

    def process_album(self):
        """Check an album for quantity and completeness."""
        quantity = True
        completeness = True
        if self.job.filter.album_min and not self.check_quantity():
            quantity = False
        if self.job.filter.album_complete and not self.check_completeness():
            completeness = False

        if quantity and completeness:
            for p in self.virtual_album:
                do_job_on_audiofile(p['path'], job=self.job)

        self.virtual_album = []

    def make_bundles(self, path=''):
        """
        :params str path: The path of the tracks.
        """
        if not path:
            self.process_album()
            return

        try:
            media = MediaFile(path)
            record = {}
            record['title'] = media.album
            record['track'] = media.track
            record['path'] = path
            if not self.current_album_title or \
                    self.current_album_title != media.album:
                self.current_album_title = media.album
                self.process_album()
            self.virtual_album.append(record)
        except phrydy.mediafile.UnreadableFileError:
            pass

    def execute(self):
        """Process all files of a given path or process a single file."""

        mb_track_listing.counter = 0
        if os.path.isdir(self.job.source):
            for path, dirs, files in os.walk(self.job.source):
                dirs.sort()
                files.sort()
                for file_name in files:
                    p = os.path.join(path, file_name)
                    if self.check_extension(p):
                        if self.bundle_filter:
                            self.make_bundles(p)
                        else:
                            do_job_on_audiofile(p, job=self.job)

            # Process the last bundle left over
            if self.bundle_filter:
                self.make_bundles()

        else:
            p = self.job.source
            if self.check_extension(p):
                do_job_on_audiofile(p, job=self.job)
