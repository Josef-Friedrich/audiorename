"""Batch processing of the audio files."""

import os
import typing

from phrydy import MediaFileExtended

from .job import Job
from .audiofile import do_job_on_audiofile, mb_track_listing


class VirtualAlbum:

    title: str
    track: int
    path: str

    def __init__(self, title: str, track: int, path: str) -> None:
        self.title = title
        self.track = track
        self.path = path


class Batch:
    """This class first sorts all files and then walks through all files. In
    this process it tries to make bundles of files belonging to an album. This
    bundle of files is temporary stored in the attribute `virtual_album`. This
    complicated mechanism is needed for the two filters `album_complete` and
    `album_min`.
    """

    virtual_album: typing.List[VirtualAlbum] = []
    """Storage of a list of files belonging to an album."""

    current_album_title: str = ''
    """Storage for the album title of the current audio file."""

    job: Job

    bundle_filter: bool

    def __init__(self, job: Job):

        self.job = job
        self.bundle_filter = job.filters.album_complete or \
            isinstance(job.filters.album_min, int)

    def check_extension(self, path: str) -> bool:
        """Check the extension of the track.

        :params str path: The path of the tracks.
        """
        extension = self.job.filters.extension
        extension = ['.' + e for e in extension]
        if path.lower().endswith(tuple(extension)):
            return True
        else:
            return False

    def check_quantity(self):
        """Compare the number of tracks in an album with the minimal track
        threshold.
        """
        if isinstance(self.job.filters.album_min, int) and \
                len(self.virtual_album) > int(self.job.filters.album_min):
            return True
        else:
            return False

    def check_completeness(self):
        """Check if the album is complete"""
        max_track = 0
        for album in self.virtual_album:
            if album.track > max_track:
                max_track = album.track

        if len(self.virtual_album) == max_track:
            return True
        else:
            return False

    def process_album(self):
        """Check an album for quantity and completeness."""
        quantity = True
        completeness = True
        if self.job.filters.album_min and not self.check_quantity():
            quantity = False
        if self.job.filters.album_complete and not self.check_completeness():
            completeness = False

        if quantity and completeness:
            for album in self.virtual_album:
                do_job_on_audiofile(album.path, job=self.job)

        self.virtual_album = []

    def make_bundles(self, path: str = ''):
        """
        :params str path: The path of the tracks.
        """
        if not path:
            self.process_album()
            return

        try:
            media = MediaFileExtended(path)
            album = VirtualAlbum(media.album, media.track, path)
            if not self.current_album_title or \
                    self.current_album_title != media.album:
                self.current_album_title = media.album
                self.process_album()
            self.virtual_album.append(album)
        except Exception:
            pass

    def execute(self):
        """Process all files of a given path or process a single file."""

        mb_track_listing.counter = 0
        if os.path.isdir(self.job.selection.source):
            for path, dirs, files in os.walk(self.job.selection.source):
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
            p = self.job.selection.source
            if self.check_extension(p):
                do_job_on_audiofile(p, job=self.job)
