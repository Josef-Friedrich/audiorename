# -*- coding: utf-8 -*-

import os
from phrydy import MediaFile


class Bundler(object):

    def __init__(self, folder):
        self.album = []
        self.album_title = ''
        for root_path, subdirs, files in os.walk(folder):
            subdirs.sort()
            files.sort()

            album_title = ''

            for file in files:
                path = os.path.join(root_path, file)

                if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")):
                    media = MediaFile(path)
                    if not self.album_title or self.album_title != media.album:
                        self.album_title = media.album
                        self.explore_album()
                        self.album = []
                    self.album.append(path)

    def check_quantity(self, quantity=6):
        if len(self.album) > quantity:
            return True
        else:
            return False

    def check_completeness(self):
        pass

    def execute(self):
        for title in self.album:
            print(title)

    def explore_album(self):
        if self.check_quantity():
            self.execute()
