# -*- coding: utf-8 -*-

import os
from phrydy import MediaFile


class Bundler(object):

    def __init__(self, folder):
        self.album = []
        for root_path, subdirs, files in os.walk(folder):
            subdirs.sort()
            files.sort()

            album_title = ''

            for file in files:
                path = os.path.join(root_path, file)

                if path.lower().endswith((".mp3", ".m4a", ".flac", ".wma")):
                    media = MediaFile(path)
                    if not album_title or album_title != media.album:
                        album_title = media.album

                        #print(len(album))
                        self.max_album(self.album)

                        print('#### New Album###')

                        self.album = []

                    self.album.append(path)
                    print('    ' + str(media.track) + '_' + path)

    def max_album(self, album):
        if len(album) > 10:
            print(album)
