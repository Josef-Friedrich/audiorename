# -*- coding: utf-8 -*-

import os
from phrydy import MediaFile


def max_album(album):
    if len(album) > 10:
        print(album)

def bundler(folder):
    album = []
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
                    max_album(album)

                    print('#### New Album###')

                    album = []

                album.append(path)
                print('    ' + str(media.track) + '_' + path)
