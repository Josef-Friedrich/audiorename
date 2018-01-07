# -*- coding: utf-8 -*-

"""Extend the class ``MediaFile`` of the package ``phrydy``."""

import phrydy
from .args import fields as module_fields
import re
from phrydy import MediaFile
from tmep import Functions
import six
import musicbrainzngs as mbrainz


class Enrich(object):

    def __init__(self, meta):
        self.meta = meta

        mbrainz.set_useragent(
            "audiorename",
            "1.2.5",
            "https://github.com/Josef-Friedrich/audiorename",
        )

    def recording(self):
        """

        soundtrack/Pulp-Fiction/01.mp3

        .. code-block:: JSON

            {
              "recording": {
                "length": "149000",
                "id": "0480672d-4d88-4824-a06b-917ff408eabe",
                "title": "Pumpkin and Honey Bunny ..."
              }
            }

        classical/Mozart_Horn-concertos/01.mp3

        .. code-block:: JSON

            {
              "recording": {
                "length": "286826",
                "work-relation-list": [
                  {
                    "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
                    "begin": "1987-03",
                    "end": "1987-03",
                    "target": "21fe0bf0-a040-387c-a39d-369d53c251fe",
                    "ended": "true",
                    "work": {
                      "id": "21fe0bf0-a040-387c-a39d-369d53c251fe",
                      "language": "zxx",
                      "title": "Concerto [...] KV 412: I. Allegro"
                    },
                    "type": "performance"
                  }
                ],
                "id": "7886ad6c-11af-435b-8ec3-bca5711f7728",
                "title": "Konzert f\u00fcr [...] K. 386b/514: I. Allegro"
              }
            }

        """

        try:
            result = mbrainz.get_recording_by_id(self.meta.mb_trackid,
                                                 includes=['work-rels'])
            return result['recording']

        except mbrainz.ResponseError as err:
            if err.cause.code == 404:
                print("Item not found")
            else:
                print("received bad response from the MB server")

    def release(self):
        """

        soundtrack/Pulp-Fiction/01.mp3

        .. code-block:: JSON

            {
              "release": {
                "status": "Bootleg",
                "release-event-count": 1,
                "title": "Pulp Fiction",
                "country": "US",
                "cover-art-archive": {
                  "count": "1",
                  "front": "true",
                  "back": "false",
                  "artwork": "true"
                },
                "release-event-list": [
                  {
                    "date": "2005-12-01",
                    "area": {
                      "sort-name": "United States",
                      "iso-3166-1-code-list": [
                        "US"
                      ],
                      "id": "489ce91b-6658-3307-9877-795b68554c98",
                      "name": "United States"
                    }
                  }
                ],
                "release-group": {
                  "first-release-date": "1994-09-27",
                  "secondary-type-list": [
                    "Compilation",
                    "Soundtrack"
                  ],
                  "primary-type": "Album",
                  "title": "Pulp Fiction: Music From the Motion Picture",
                  "type": "Soundtrack",
                  "id": "1703cd63-9401-33c0-87c6-50c4ba2e0ba8"
                },
                "text-representation": {
                  "language": "eng",
                  "script": "Latn"
                },
                "date": "2005-12-01",
                "quality": "normal",
                "id": "ab81edcb-9525-47cd-8247-db4fa969f525",
                "asin": "B000002OTL"
              }
            }

        classical/Mozart_Horn-concertos/01.mp3

        .. code-block:: JSON

            {
              "release": {
                "status": "Official",
                "release-event-count": 1,
                "title": "4 Hornkonzerte (Concertos for Horn and Orchestra)",
                "country": "DE",
                "barcode": "028942781429",
                "cover-art-archive": {
                  "count": "0",
                  "front": "false",
                  "back": "false",
                  "artwork": "false"
                },
                "release-event-list": [
                  {
                    "date": "1988",
                    "area": {
                      "sort-name": "Germany",
                      "iso-3166-1-code-list": [
                        "DE"
                      ],
                      "id": "85752fda-13c4-31a3-bee5-0e5cb1f51dad",
                      "name": "Germany"
                    }
                  }
                ],
                "release-group": {
                  "first-release-date": "1988",
                  "title": "4 Hornkonzerte (Concertos for Horn and Orchestra)",
                  "type": "Album",
                  "id": "e1fa28f0-e56e-395b-82d3-a8de54e8c627",
                  "primary-type": "Album"
                },
                "text-representation": {
                  "language": "deu",
                  "script": "Latn"
                },
                "date": "1988",
                "quality": "normal",
                "id": "5ed650c5-0f72-4b79-80a7-c458c869f53e",
                "asin": "B00000E4FA"
              }
            }

            """

        try:
            result = mbrainz.get_release_by_id(self.meta.mb_albumid,
                                               includes=['release-groups'])
            return result['release']

        except mbrainz.ResponseError as err:
            if err.cause.code == 404:
                print("Item not found")
            else:
                print("received bad response from the MB server")

        # def work_hierachy(self):
        #     if self.meta.mb_workid:
        #         work_id = self.meta.mb_workid
        #     else:
        #         recording = self.recording()


def work_recursion(work_id, works=[]):
    # https://musicbrainz.org/recording/6a0599ea-5c06-483a-ba66-f3a036da900a

    """
    .. code-block:: JSON

        {
          "work": {
            "work-relation-list": [
              {
                "type-id": "ca8d3642-ce5f-49f8-91f2-125d72524e6a",
                "direction": "backward",
                "target": "5adc213f-700a-4435-9e95-831ed720f348",
                "ordering-key": "3",
                "work": {
                  "id": "5adc213f-700a-4435-9e95-831ed720f348",
                  "language": "deu",
                  "title": "Die Zauberfl\u00f6te, K. 620: Akt I"
                },
                "type": "parts"
              },
              {
                "type-id": "51975ed8-bbfa-486b-9f28-5947f4370299",
                "work": {
                  "disambiguation": "for piano, arr. Matthias",
                  "id": "798f4c25-0ab3-44ba-81b6-3d856aedf82a",
                  "language": "zxx",
                  "title": "Die Zauberfl\u00f6te, K. 620: Aria ..."
                },
                "type": "arrangement",
                "target": "798f4c25-0ab3-44ba-81b6-3d856aedf82a"
              }
            ],
            "type": "Aria",
            "id": "eafec51f-47c5-3c66-8c36-a524246c85f8",
            "language": "deu",
            "title": "Die Zauberfl\u00f6te: Act I, Scene II. No. 2 Aria ..."
          }
        }
    """

    try:

        mbrainz.set_useragent(
            "audiorename",
            "1.2.5",
            "https://github.com/Josef-Friedrich/audiorename",
        )
        result = mbrainz.get_work_by_id(work_id,
                                        includes=['work-rels'])
        work = result['work']
        works.append({'id': work['id'], 'title': work['title']})

        parent_work = False
        if work['work-relation-list']:
            for relation in work['work-relation-list']:
                if 'direction' in relation and \
                        relation['direction'] == 'backward':
                    parent_work = relation
                    break

        if parent_work:
            work_recursion(parent_work['work']['id'], works)

    except mbrainz.ResponseError as err:
        if err.cause.code == 404:
            print("Item not found")
        else:
            print("Received bad response from the MB server")

    return works


class Meta(MediaFile):

    def __init__(self, path, shell_friendly=False):
        super(Meta, self).__init__(path, False)
        self.shell_friendly = shell_friendly

###############################################################################
# Public methods
###############################################################################

    def export_dict(self):
        fields = phrydy.doc.merge_fields(phrydy.doc.fields, module_fields)
        out = {}
        for field, description in sorted(fields.items()):
            value = getattr(self, field)
            if value:
                out[field] = self._sanitize(value)
            else:
                out[field] = u''

        return out

    def enrich_metadata(self):
        """Get the work title and the work id of a track.

        Internal used dictionary:

        .. code-block:: Python

            {
                'recording': {
                    'length': '566933',
                    'work-relation-list': [
                        {
                            'type-id': 'a3005666-a872-32c3-ad06-98af558e99b0',
                            'work': {
                                'id': '6b198406-4fbf-3d61-82db-0b7ef195a7fe',
                                'language': 'zxx',
                                'title': u'Die Meistersinger von ....'
                            },
                            'type': 'performance',
                            'target': '6b198406-4fbf-3d61-82db-0b7ef195a7fe'
                        }
                    ],
                    'id': '00ba1660-4e35-4985-86b2-8b7a3e99b1e5',
                    'title': u'Die Meistersinger von N\xfcrnberg: Vorspiel'
                }
            }
        """

        mbrainz.set_useragent(
            "audiorename",
            "1.0.8",
            "https://github.com/Josef-Friedrich/audiorename",
        )

        try:
            result = mbrainz.get_recording_by_id(self.mb_trackid,
                                                 includes=['work-rels'])
            if 'recording' in result and \
                    'work-relation-list' in result['recording'] and \
                    len(result['recording']['work-relation-list']) > 0:
                work = result['recording']['work-relation-list'][0]
                self.mb_workid = work['work']['id']
                self.work = work['work']['title']
            else:
                print("Work relation doesn’t exist.")

        except mbrainz.ResponseError as err:
            if err.cause.code == 404:
                print("Work not found")
            else:
                print("received bad response from the MB server")

    def remap_classical(self):
        pass

###############################################################################
# Static methods
###############################################################################

    @staticmethod
    def _initials(value):
        """
        :param str value: A string to extract the initials.
        """
        return value[0:1].lower()

    @staticmethod
    def _normalize_performer(performer):
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
    def _roman_to_int(n):
        numeral_map = tuple(zip(
            (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
            ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV',
             'I')
        ))
        i = result = 0
        for integer, numeral in numeral_map:
            while n[i:i + len(numeral)] == numeral:
                result += integer
                i += len(numeral)
        return result

    @staticmethod
    def _sanitize(value):
        if isinstance(value, str) or \
                (six.PY2 and isinstance(value, unicode)) or \
                (six.PY3 and isinstance(value, bytes)):
            value = Functions.tmpl_sanitize(value)
            value = re.sub(r'\s{2,}', ' ', value)
        else:
            value = u''
        return value

    @staticmethod
    def _shorten_performer(performer, length=3, separator=u' ',
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

    @staticmethod
    def _unify_list(seq):
        """https://www.peterbe.com/plog/uniqifiers-benchmark"""
        noDupes = []
        [noDupes.append(i) for i in seq if not noDupes.count(i)]
        return noDupes

###############################################################################
# Properties
###############################################################################

    @property
    def album_classical(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.work``

        Examples:

        * ``Horn Concerto: I. Allegro`` → ``I. Allegro``
        * ``Die Meistersinger von Nürnberg``
        """
        if self.work:
            return re.sub(r':.*$', '', (str(self.work)))
        else:
            return u''

    @property
    def album_clean(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.album``

        Example:

        * ``Just Friends (Disc 2)`` → ``Just Friends``
        """
        if self.album:
            return re.sub(r' ?\([dD]is[ck].*\)$', '', str(self.album))
        else:
            return u''

    @property
    def album_initial(self):
        """Uses:

        * :class:`audiorename.meta.Meta.album_clean`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        return self._initials(self.album_clean)

    @property
    def artist_initial(self):
        """Uses:

        * :class:`audiorename.meta.Meta.artistsafe_sort`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        return self._initials(self.artistsafe_sort)

    @property
    def artistsafe(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.albumartist``
        * ``phrydy.mediafile.MediaFile.artist``
        * ``phrydy.mediafile.MediaFile.albumartist_credit``
        * ``phrydy.mediafile.MediaFile.artist_credit``
        * ``phrydy.mediafile.MediaFile.albumartist_sort``
        * ``phrydy.mediafile.MediaFile.artist_sort``
        """
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
        """Uses:

        * ``phrydy.mediafile.MediaFile.albumartist_sort``
        * ``phrydy.mediafile.MediaFile.artist_sort``
        * ``phrydy.mediafile.MediaFile.albumartist``
        * ``phrydy.mediafile.MediaFile.artist``
        * ``phrydy.mediafile.MediaFile.albumartist_credit``
        * ``phrydy.mediafile.MediaFile.artist_credit``
        """
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

        if self.shell_friendly:
            out = out.replace(', ', '_')

        return out

    @property
    def composer_initial(self):
        """Uses:

        * :class:`audiorename.meta.Meta.composer_safe`
        """
        return self._initials(self.composer_safe)

    @property
    def composer_safe(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.composer_sort``
        * ``phrydy.mediafile.MediaFile.composer``
        * :class:`audiorename.meta.Meta.artistsafe`
        """
        if self.composer_sort:
            out = self.composer_sort
        elif self.composer:
            out = self.composer
        else:
            out = self.artistsafe

        if self.shell_friendly:
            out = out.replace(', ', '_')

        # e. g. 'Mozart, Wolfgang Amadeus/Süßmeyer, Franz Xaver'
        return re.sub(r' ?/.*', '', out)

    @property
    def disctrack(self):
        """
        Generate a combination of track and disc number, e. g.: ``1-04``,
        ``3-06``.

        Uses:

        * ``phrydy.mediafile.MediaFile.disctotal``
        * ``phrydy.mediafile.MediaFile.disc``
        * ``phrydy.mediafile.MediaFile.tracktotal``
        * ``phrydy.mediafile.MediaFile.track``
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
        """Uses:

        * :class:`audiorename.meta.Meta.performer_raw`
        """
        out = u''
        for performer in self.performer_raw:
            out = out + u', ' + performer[1]

        out = out[2:]

        return out

    @property
    def performer_classical(self):
        """http://musicbrainz.org/doc/Style/Classical/Release/Artist

        Uses:

        * :class:`audiorename.meta.Meta.performer_short`
        * ``phrydy.mediafile.MediaFile.albumartist``
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

        Uses:

        * ``phrydy.mediafile.MediaFile.mgfile``
        """
        out = []

        if (self.format == 'FLAC' or self.format == 'OGG') and \
                'performer' in self.mgfile:
            out = self._normalize_performer(self.mgfile['performer'])
            if 'conductor' in self.mgfile:
                out.insert(0, [u'conductor', self.mgfile['conductor'][0]])
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
                out.insert(0, [u'conductor', self.mgfile['TPE3'].text[0]])

        else:
            out = []

        return self._unify_list(out)

    @property
    def performer_short(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.performer_raw``
        """
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
                s = self._shorten_performer(p[1], separator=u'',
                                            abbreviation=u'')
            else:
                s = p[1].split(' ')[-1]
            out = out + u', ' + s

        out = out[2:]

        return out

    @property
    def soundtrack(self):
        if (self.albumtype and u'soundtrack' in self.albumtype.lower()) or \
                (self.genre and u'soundtrack' in self.genre.lower()):
            return True
        else:
            return False

    @property
    def title_classical(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.title``

        Example:

        * ``Horn Concerto: I. Allegro``
        """
        if self.title:
            return re.sub(r'^[^:]*: ?', '', self.title)
        else:
            return u''

    @property
    def track_classical(self):
        """Uses:

        * :class:`audiorename.meta.Meta.title_classical`
        * :class:`audiorename.meta.Meta.disctrack`
        """
        roman = re.findall(r'^([IVXLCDM]*)\.', self.title_classical)
        if roman:
            out = str(self._roman_to_int(roman[0])).zfill(2)
        elif self.disctrack:
            out = self.disctrack
        else:
            out = ''

        return out

    @property
    def year_safe(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.original_year``
        * ``phrydy.mediafile.MediaFile.year``
        """
        if self.original_year:
            out = self.original_year
        elif self.year:
            out = self.year
        else:
            out = ''
        return str(out)
