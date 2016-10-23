# -*- coding: utf-8 -*-
import phrydy
from phrydy import MediaFile
from tmep import Functions
import six


class Meta(object):

    def __init__(self, path=False, shell_friendly=False):
        self.path = path
        self.shell_friendly = shell_friendly

    def getMediaFile(self):
        meta = {}
        try:
            meta['skip'] = False
            self.media_file = MediaFile(self.path)
            for key in MediaFile.readable_fields():
                value = getattr(self.media_file, key)
                if key != 'art':
                    if six.PY2:
                        if not value:
                            value = ''
                        elif \
                                isinstance(value, str) or \
                                isinstance(value, unicode):
                            value = Functions.tmpl_sanitize(value)
                    else:
                        if not value:
                            value = ''
                        elif \
                                isinstance(value, bytes) or \
                                isinstance(value, str):
                            value = Functions.tmpl_sanitize(value)
                    meta[key] = value

        except phrydy.UnreadableFileError:
            meta['skip'] = True

        return meta

    def discTrack(self, meta):
        if meta['disctotal'] and int(meta['disctotal']) > 9:
            disk = str(meta['disc']).zfill(2)
        else:
            disk = str(meta['disc'])

        if meta['tracktotal'] and int(meta['tracktotal']) > 99:
            track = str(meta['track']).zfill(3)
        else:
            track = str(meta['track']).zfill(2)

        if meta['disc'] and meta['disctotal'] and int(meta['disctotal']) > 1:
            return disk + '-' + track
        else:
            return track

    def artistSafe(self, meta):
        safe = ''
        if meta['albumartist']:
            safe = meta['albumartist']
        elif meta['artist']:
            safe = meta['artist']
        elif meta['albumartist_credit']:
            safe = meta['albumartist_credit']
        elif meta['artist_credit']:
            safe = meta['artist_credit']

        sort = ''
        if meta['albumartist_sort']:
            sort = meta['albumartist_sort']
        elif meta['artist_sort']:
            sort = meta['artist_sort']
        if self.shell_friendly:
            sort = value.replace(', ', '_')

        if not sort and not safe:
            sort = safe = 'Unknown'

        if not sort:
            sort = safe

        if not safe:
            safe = sort

        return safe, sort

    def yearSafe(self, meta):
        if meta['original_year']:
            value = meta['original_year']
        elif meta['year']:
            value = meta['year']
        else:
            value = ''
        return value

    def initials(self, value):
        return value[0:1].lower()

    def getMeta(self):
        meta = self.getMediaFile()

        if not meta['skip']:
            meta['disctrack'] = self.discTrack(meta)
            meta['artistsafe'], meta['artistsafe_sort'] = self.artistSafe(meta)
            meta['year_safe'] = self.yearSafe(meta)
            meta['artist_initial'] = self.initials(meta['artistsafe_sort'])
            meta['album_initial'] = self.initials(meta['album'])
            return meta
        else:
            return False
