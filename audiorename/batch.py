# -*- coding: utf-8 -*-

from .rename import do_rename
from phrydy import MediaFile
import os


class Batch(object):

    def __init__(self, args):
        self.args = args
        self.album = []
        self.album_title = ''

    def execute_album(self):
        quantity = True
        completeness = True
        if self.args.filter_album_min and not self.check_quantity():
            quantity = False
        if self.args.filter_album_complete and not self.check_completeness():
            completeness = False

        if quantity and completeness:
            for p in self.album:
                do_rename(p['path'], args=self.args)

    def make_bundles(self, path, finish=False):
        if finish:
            self.execute_album()
            self.album = []
            return

        media = MediaFile(path)
        record = {}
        record['title'] = media.album
        record['track'] = media.track
        record['path'] = path
        if not self.album_title or self.album_title != media.album:
            self.album_title = media.album
            self.execute_album()
            self.album = []
        self.album.append(record)

    def check_extension(self, path):
        if path.lower().endswith(('.mp3', '.m4a', '.flac', '.wma')):
            return True
        else:
            return False

    def check_quantity(self):
        if len(self.album) > int(self.args.filter_album_min):
            return True
        else:
            return False

    def check_completeness(self):
        max_track = 0
        for record in self.album:
            if record['track'] > max_track:
                max_track = record['track']

        if len(self.album) == max_track:
            return True
        else:
            return False

    def execute(self):
        if self.args.is_dir:
            for path, dirs, files in os.walk(self.args.path):
                dirs.sort()
                files.sort()
                for file_name in files:
                    p = os.path.join(path, file_name)
                    if self.check_extension(p):
                        if self.args.filter:
                            self.make_bundles(p)
                        else:
                            do_rename(p, args=self.args)

            if self.args.filter:
                self.make_bundles('', True)

        else:
            p = self.args.path
            if self.check_extension(p):
                do_rename(p, args=self.args)
