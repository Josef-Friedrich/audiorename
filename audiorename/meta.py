# -*- coding: utf-8 -*-
from phrydy import MediaFile
from tmep import Functions
import six


class Meta(object):
    def __init__(self, path, shell_friendly=False):

        self.shell_friendly = shell_friendly

        self.media_file = MediaFile(path)
        self.m = {}
        for key in MediaFile.readable_fields():
            value = getattr(self.media_file, key)
            if key != 'art':
                if six.PY2:
                    if not value:
                        value = ''
                    elif isinstance(value, str) or isinstance(value, unicode):
                        value = Functions.tmpl_sanitize(value)
                else:
                    if not value:
                        value = ''
                    elif isinstance(value, bytes) or isinstance(value, str):
                        value = Functions.tmpl_sanitize(value)
                self.m[key] = value
        self.discTrack()
        self.artistSafe()
        self.yearSafe()
        self.initials()

    def discTrack(self):
        if self.m['disctotal'] > 9:
            disk = str(self.m['disc']).zfill(2)
        else:
            disk = str(self.m['disc'])

        if self.m['tracktotal'] > 99:
            track = str(self.m['track']).zfill(3)
        else:
            track = str(self.m['track']).zfill(2)

        if self.m['disc'] and self.m['disctotal'] > 1:
            self.m['disctrack'] = disk + '-' + track
        else:
            self.m['disctrack'] = track

    def artistSafe(self):
        safe_sort = ''
        safe = ''
        if self.m['albumartist_sort']:
            safe_sort = self.m['albumartist_sort']
        elif self.m['artist_sort']:
            safe_sort = self.m['artist_sort']

        if self.m['albumartist']:
            safe = self.m['albumartist']
        elif self.m['artist']:
            safe = self.m['artist']
        elif self.m['albumartist_credit']:
            safe = self.m['albumartist_credit']
        elif self.m['artist_credit']:
            safe = self.m['artist_credit']

        if not safe_sort:
            if safe:
                safe_sort = safe
            else:
                safe_sort = 'Unknown'

        if self.shell_friendly:
            safe_sort = safe_sort.replace(', ', '_')

        self.m['artistsafe'] = safe
        self.m['artistsafe_sort'] = safe_sort

    def yearSafe(self):
        if self.m['original_year']:
            value = self.m['original_year']
        elif self.m['year']:
            value = self.m['year']
        else:
            value = ''
        self.m['year_safe'] = value

    def initials(self):
        self.m['artist_initial'] = self.m['artistsafe_sort'][0:1].lower()
        self.m['album_initial'] = self.m['album'][0:1].lower()

    def getMeta(self):
        return self.m
