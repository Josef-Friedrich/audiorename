# -*- coding: utf-8 -*-

"""Batch processing of the audio files."""

from .rename import do_rename
import phrydy
from phrydy import MediaFile
import os


class Batch(object):

    def __init__(self, args, job):
        self.args = args
        self.job = job
        self.album = []
        self.album_title = ''

    def check_extension(self, path):
        """Check the extension of the track.

        :params str path: The path of the tracks.
        """
        extension = self.args.extension.split(',')
        extension = ['.' + e for e in extension]
        if path.lower().endswith(tuple(extension)):
            return True
        else:
            return False

    def check_quantity(self):
        """Compare the number of tracks in an album with the minimal track
        threshold.
        """
        if len(self.album) > int(self.args.album_min):
            return True
        else:
            return False

    def check_completeness(self):
        """Check if the album is complete"""
        max_track = 0
        for record in self.album:
            if record['track'] > max_track:
                max_track = record['track']

        if len(self.album) == max_track:
            return True
        else:
            return False

    def check_album(self):
        """Check an album for quantity and completeness."""
        quantity = True
        completeness = True
        if self.args.album_min and not self.check_quantity():
            quantity = False
        if self.args.album_complete and not self.check_completeness():
            completeness = False

        if quantity and completeness:
            for p in self.album:
                do_rename(p['path'], args=self.args)

        self.album = []

    def make_bundles(self, path=''):
        """
        :params str path: The path of the tracks.
        """
        if not path:
            self.check_album()
            return

        try:
            media = MediaFile(path)
            record = {}
            record['title'] = media.album
            record['track'] = media.track
            record['path'] = path
            if not self.album_title or self.album_title != media.album:
                self.album_title = media.album
                self.check_album()
            self.album.append(record)
        except phrydy.mediafile.UnreadableFileError:
            pass

    def execute(self):
        """Process all files of a given path or process a single file."""
        if os.path.isdir(self.job.source):
            for path, dirs, files in os.walk(self.job.source):
                dirs.sort()
                files.sort()
                for file_name in files:
                    p = os.path.join(path, file_name)
                    if self.check_extension(p):
                        if self.args.filter:
                            self.make_bundles(p)
                        else:
                            do_rename(p, args=self.args, job=self.job)

            # Process the last bundle left over
            if self.args.filter:
                self.make_bundles()

        else:
            p = self.job.source
            if self.check_extension(p):
                do_rename(p, args=self.args, job=self.job)
