# -*- coding: utf-8 -*-

"""Extend the class ``MediaFile`` of the package ``phrydy``."""

import phrydy
from .args import fields as module_fields
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


def meta_to_dict(meta):
    fields = phrydy.doc.fields.copy()
    fields.update(module_fields)
    out = {}
    for field, description in sorted(fields.items()):
        value = getattr(meta, field)
        if value:
            out[field] = value
        else:
            out[field] = u''

    return out


class Meta(MediaFile):

    def __init__(self, path, args=False):
        super(Meta, self).__init__(path, False)
        self.args = args

###############################################################################
# Static methods
###############################################################################

    @staticmethod
    def initials(value):
        """
        :param str value: A string to extract the initials.
        """
        return value[0:1].lower()

    @staticmethod
    def normalizePerformer(performer):
        """
        :param list performer: A list of raw performer strings like

        .. code-block:: python

            [u'John Lennon (vocals)', u'Ringo Starr (drums)']

        :return: A list

        .. code-block:: python

            [
                ['vocals', u'John Lennon'],
                ['drums', u'Ringo Starr'],
            ]
        """
        out = []
        if isinstance(performer, list):
            for value in performer:
                value = value[:-1]
                value = value.split(u' (')
                if isinstance(value, list) and len(value) == 2:
                    out.append([value[1], value[0]])
            return out
        else:
            return []

    @staticmethod
    def sanitize(value):
        if isinstance(value, str) or \
                (six.PY2 and isinstance(value, unicode)) or \
                (six.PY3 and isinstance(value, bytes)):
            value = Functions.tmpl_sanitize(value)
            value = re.sub(r'\s{2,}', ' ', value)
        else:
            value = u''
        return value

    @staticmethod
    def shortenPerformer(performer, length=3, separator=u' ',
                         abbreviation=u'.'):
        out = u''
        count = 0
        for s in performer.split(' '):
            if count < 3:
                if len(s) > length:
                    part = s[:length] + abbreviation
                else:
                    part = s
                out = out + separator + part
            count = count + 1

        return out[len(separator):]

###############################################################################
# Properties
###############################################################################

    @property
    def album_classical(self):
        """Example: ``Horn Concerto: I. Allegro``
        """
        return re.sub(r':.*$', '', (str(self.work)))

    @property
    def album_clean(self):
        return re.sub(r' ?\([dD]is[ck].*\)$', '', self.album)

    @property
    def album_initial(self):
        return self.initials(self.album_clean)

    @property
    def artist_initial(self):
        return self.initials(self.artistsafe_sort)

    @property
    def artistsafe(self):
        if self.albumartist:
            out = self.albumartist
        elif self.artist:
            out = self.artist
        elif self.albumartist_credit:
            out = self.albumartist_credit
        elif self.artist_credit:
            out = self.artist_credit
        # Same as aristsafe_sort
        elif self.albumartist_sort:
            out = self.albumartist_sort
        elif self.artist_sort:
            out = self.artist_sort
        else:
            out = u'Unknown'

        return out

    @property
    def artistsafe_sort(self):
        out = ''
        if self.albumartist_sort:
            out = self.albumartist_sort
        elif self.artist_sort:
            out = self.artist_sort
        # Same as artistsafe
        elif self.albumartist:
            out = self.albumartist
        elif self.artist:
            out = self.artist
        elif self.albumartist_credit:
            out = self.albumartist_credit
        elif self.artist_credit:
            out = self.artist_credit
        else:
            out = u'Unknown'

        if self.args.shell_friendly:
            out = out.replace(', ', '_')

        return out

    @property
    def composer_initial(self):
        return self.initials(self.composer_safe)

    @property
    def composer_safe(self):
        if self.composer_sort:
            out = self.composer_sort
        elif self.composer:
            out = self.composer
        else:
            out = self.artistsafe

        if self.args.shell_friendly:
            out = out.replace(', ', '_')

        # e. g. 'Mozart, Wolfgang Amadeus/Süßmeyer, Franz Xaver'
        return re.sub(r' ?/.*', '', out)

    @property
    def disctrack(self):
        """
        Generate a combination of track and disc number, e. g.: ``1-04``,
        ``3-06``.
        """

        if not self.track:
            return ''

        if self.disctotal and int(self.disctotal) > 99:
            disk = str(self.disc).zfill(3)
        elif self.disctotal and int(self.disctotal) > 9:
            disk = str(self.disc).zfill(2)
        else:
            disk = str(self.disc)

        if self.tracktotal and int(self.tracktotal) > 99:
            track = str(self.track).zfill(3)
        else:
            track = str(self.track).zfill(2)

        if self.disc and self.disctotal and int(self.disctotal) > 1:
            out = disk + '-' + track
        elif self.disc and not self.disctotal:
            out = disk + '-' + track
        else:
            out = track

        return out

    @property
    def performer(self):
        out = u''
        for performer in self.performer_raw:
            out = out + u', ' + performer[1]

        out = out[2:]

        return out

    @property
    def performer_classical(self):
        """http://musicbrainz.org/doc/Style/Classical/Release/Artist
        """
        if len(self.performer_short) > 0:
            out = self.performer_short
        elif self.albumartist:
            out = re.sub(r'^.*; ?', '', self.albumartist)
        else:
            out = u''

        return out

    @property
    def performer_raw(self):
        """Generate a unifed performer list.

        Picard doesn’t store performer values in m4a, alac.m4a, wma, wav,
        aiff.

        :return: A list

        .. code-block:: python

            [
                ['conductor', u'Herbert von Karajan'],
                ['violin', u'Anne-Sophie Mutter'],
            ]

        """
        out = []

        if (self.format == 'FLAC' or self.format == 'OGG') and \
                'performer' in self.mgfile:
            out = self.normalizePerformer(self.mgfile['performer'])
            if 'conductor' in self.mgfile:
                out.insert(0, ['conductor', self.mgfile['conductor'][0]])
        elif self.format == 'MP3':
            # 4.2.2 TMCL Musician credits list
            if 'TMCL' in self.mgfile:
                out = self.mgfile['TMCL'].people
            # 4.2.2 TIPL Involved people list
            # TIPL is used for producer
            elif 'TIPL' in self.mgfile:
                out = self.mgfile['TIPL'].people

            # 4.2.2 TPE3 Conductor/performer refinement
            if len(out) > 0 and 'conductor' not in out[0] \
                    and 'TPE3' in self.mgfile:
                out.insert(0, ['conductor', self.mgfile['TPE3'].text[0]])

        else:
            out = []

        return out

    @property
    def performer_short(self):
        out = u''

        performer = self.performer_raw
        picked = []
        for p in performer:
            if p[0] == u'conductor' or p[0] == u'orchestra':
                picked.append(p)

        if len(picked) > 0:
            performer = picked

        for p in performer:

            if p[0] == u'producer' or p[0] == u'executive producer' or \
                    p[0] == 'balance engineer':
                s = u''
            elif p[0] == u'orchestra' or p[0] == u'choir vocals' or \
                    p[0] == 'string quartet':
                s = self.shortenPerformer(p[1], separator=u'',
                                          abbreviation=u'')
            else:
                s = p[1].split(' ')[-1]
            out = out + u', ' + s

        out = out[2:]

        return out

    @property
    def title_classical(self):
        """Example: ``Horn Concerto: I. Allegro``
        """
        return re.sub(r'^[^:]*: ?', '', self.title)

    @property
    def track_classical(self):
        roman = re.findall(r'^([IVXLCDM]*)\.', self.title_classical)
        if roman:
            out = str(roman_to_int(roman[0])).zfill(2)
        elif self.disctrack:
            out = self.disctrack
        else:
            out = ''

        return out

    @property
    def year_safe(self):
        if self.original_year:
            out = self.original_year
        elif self.year:
            out = self.year
        else:
            out = ''
        return str(out)
