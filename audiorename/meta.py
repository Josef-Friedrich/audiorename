# -*- coding: utf-8 -*-

"""Extend the class ``MediaFile`` of the package ``phrydy``."""

import phrydy
import re
from phrydy import MediaFile
from tmep import Functions
import six


def roman_to_int(n):
    numeral_map = tuple(zip(
        (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
        ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    ))
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result


"""
:param str path: The absolute path of the audio file.
:param bool shell_friendly: Generate shell friendly strings.
"""


class Meta(object):

    def __init__(self, path=False, shell_friendly=False):
        self.path = path
        self.shell_friendly = shell_friendly

    def getMediaFile(self):
        """Use the ``MediaFile`` class of the package ``phrydy`` to retrieve all
        metadata informations and save this values in a dictionary.
        """
        meta = {}
        try:
            meta['skip'] = False
            self.media_file = MediaFile(self.path)
            for key in MediaFile.readable_fields():
                value = getattr(self.media_file, key)
                if key != 'art':
                    if not value:
                        value = ''
                    meta[key] = value

        except phrydy.mediafile.UnreadableFileError:
            meta['skip'] = True

        return meta

    def sanitize(self, meta):
        output = {}
        for key, value in meta.items():
            if isinstance(value, str) or \
                    (six.PY2 and isinstance(value, unicode)) or \
                    (six.PY3 and isinstance(value, bytes)):
                value = Functions.tmpl_sanitize(value)
                value = re.sub(r'\s{2,}', ' ', value)

            output[key] = value
        return output

    def initials(self, value):
        """
        :param str value: A string to extract the initials.
        """
        return value[0:1].lower()

    def albumClassical(self, value):
        """Example: ``Horn Concerto: I. Allegro``

        :param str value: The title string.
        """
        return re.sub(r':.*$', '', value)

    def albumClean(self, album):
        """
        :param str album: The text of the album.
        """
        album = re.sub(r' ?\([dD]is[ck].*\)$', '', album)
        return album

    def artistSafe(self, meta):
        """
        :param dict meta: A dictionary with meta informations.
        """
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
            sort = sort.replace(', ', '_')

        if not sort and not safe:
            sort = safe = 'Unknown'

        if not sort:
            sort = safe

        if not safe:
            safe = sort

        return safe, sort

    def composerSafe(self, meta):
        if meta['composer_sort']:
            value = meta['composer_sort']
        elif meta['composer']:
            value = meta['composer']
        else:
            value = meta['artistsafe']

        if self.shell_friendly:
            value = value.replace(', ', '_')

        # e. g. 'Mozart, Wolfgang Amadeus/Süßmeyer, Franz Xaver'
        return re.sub(r' ?/.*', '', value)

    def discTrack(self, meta):
        """
        Generate a combination of track and disc number, e. g.: ``1-04``,
        ``3-06``.

        :param dict meta: A dictionary with meta informations.
        """
        m = meta

        if not m['track']:
            return ''

        if m['disctotal'] and int(m['disctotal']) > 99:
            disk = str(m['disc']).zfill(3)
        elif m['disctotal'] and int(m['disctotal']) > 9:
            disk = str(m['disc']).zfill(2)
        else:
            disk = str(m['disc'])

        if m['tracktotal'] and int(m['tracktotal']) > 99:
            track = str(m['track']).zfill(3)
        else:
            track = str(m['track']).zfill(2)

        if m['disc'] and m['disctotal'] and int(m['disctotal']) > 1:
            return disk + '-' + track
        elif m['disc'] and not m['disctotal']:
            return disk + '-' + track
        else:
            return track

    def titleClassical(self, value):
        """Example: ``Horn Concerto: I. Allegro``

        :param str value: The title string.
        """
        return re.sub(r'^[^:]*: ?', '', value)

    def trackClassical(self, title, disc_track=False):
        roman = re.findall(r'^([IVXLCDM]*)\.', title)
        if roman:
            return roman_to_int(roman[0])
        elif disc_track:
            return disc_track
        else:
            return ''

    def yearSafe(self, meta):
        """
        :param dict meta: A dictionary with meta informations.
        """
        if meta['original_year']:
            value = meta['original_year']
        elif meta['year']:
            value = meta['year']
        else:
            value = ''
        return value

    def getMeta(self):
        meta = self.getMediaFile()

        if not meta['skip']:

            # album
            meta['album_classical'] = self.albumClassical(meta['work'])
            meta['album_clean'] = self.albumClean(meta['album'])
            meta['album_initial'] = self.initials(meta['album_clean'])

            # artist
            meta['artistsafe'], meta['artistsafe_sort'] = self.artistSafe(meta)
            meta['artist_initial'] = self.initials(meta['artistsafe_sort'])

            # composer
            meta['composer_safe'] = self.composerSafe(meta)
            meta['composer_initial'] = self.initials(meta['composer_safe'])

            meta['disctrack'] = self.discTrack(meta)
            meta['title_classical'] = self.titleClassical(meta['title'])
            meta['track_classical'] = self.trackClassical(
                meta['title_classical'],
                meta['disctrack']
            )
            meta['year_safe'] = self.yearSafe(meta)
            return self.sanitize(meta)
        else:
            return False
