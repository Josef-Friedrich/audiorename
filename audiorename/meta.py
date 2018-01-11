# -*- coding: utf-8 -*-

"""Extend the class ``MediaFile`` of the package ``phrydy``.

``get_recording_by_id`` with ``work-rels``

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

``get_work_by_id`` with ``work-rels``

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
        "title": "Die Zauberfl\u00f6te: Act I, Scene II. No. 2 Aria .."
      }
    }


.. code-block:: JSON

    {
      "work": {
        "work-relation-list": [
          {
            "type-id": "c1dca2cd-194c-36dd-93f8-6a359167e992",
            "direction": "backward",
            "work": {
              "id": "70e53569-258c-463d-9505-5b69dcbf374a",
              "title": "Can\u2019t Stop the Classics, Part 2"
            },
            "type": "medley",
            "target": "70e53569-258c-463d-9505-5b69dcbf374a"
          },
          {
            "type-id": "ca8d3642-ce5f-49f8-91f2-125d72524e6a",
            "direction": "backward",
            "target": "73663bd3-392f-45a7-b4ff-e75c01f5926a",
            "ordering-key": "1",
            "work": {
              "id": "73663bd3-392f-45a7-b4ff-e75c01f5926a",
              "language": "deu",
              "title": "Die Meistersinger von N\u00fcrnberg, WWV 96: Akt I"
            },
            "type": "parts"
          }
        ]
      }
    }

``get_release_by_id`` with ``release-groups``

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

import re
from phrydy import MediaFile
from tmep import Functions
import six
import musicbrainzngs as mbrainz
from ._version import get_versions


def set_useragent():
    mbrainz.set_useragent(
        'audiorename',
        get_versions()['version'],
        'https://github.com/Josef-Friedrich/audiorename',
    )


def query_mbrainz(mb_type, mb_id):
    method = 'get_' + mb_type + '_by_id'
    query = getattr(mbrainz, method)

    if mb_type == 'recording' or mb_type == 'work':
        mb_includes = ['work-rels']
    elif mb_type == 'release':
        mb_includes = ['release-groups']
    else:
        mb_includes = []

    try:
        result = query(mb_id, includes=mb_includes)
        return result[mb_type]

    except mbrainz.ResponseError as err:
        if err.cause.code == 404:
            print('Item of type “' + mb_type + '” with the ID “' +
                  mb_id + '” not found.')
        else:
            print("Received bad response from the MusicBrainz server.")


def work_recursion(work_id, works=[]):
    work = query_mbrainz('work', work_id)

    if not work:
        return works

    works.append({'id': work['id'], 'title': work['title']})

    parent_work = False
    if 'work-relation-list' in work:
        for relation in work['work-relation-list']:
            if 'direction' in relation and \
                    relation['direction'] == 'backward' and \
                    relation['type'] != 'medley':
                parent_work = relation
                break

    if parent_work:
        work_recursion(parent_work['work']['id'], works)

    return works


class Meta(MediaFile):

    def __init__(self, path, shell_friendly=False):
        super(Meta, self).__init__(path, False)
        self.shell_friendly = shell_friendly

###############################################################################
# Public methods
###############################################################################

    def export_dict(self):
        out = {}
        for field in self.fields_sorted():
            value = getattr(self, field)
            if value:
                out[field] = self._sanitize(str(value))
            else:
                out[field] = u''

        return out

    def enrich_metadata(self):
        set_useragent()

        if self.mb_trackid:
            recording = query_mbrainz('recording', self.mb_trackid)

        if self.mb_albumid:
            release = query_mbrainz('release', self.mb_albumid)
        if 'release-group' in release:
            release_group = release['release-group']
            types = []
            if 'type' in release_group:
                types.append(release_group['type'])
            if 'primary-type' in release_group:
                types.append(release_group['primary-type'])
            if 'secondary-type-list' in release_group:
                types = types + release_group['secondary-type-list']
            types = self._unify_list(types)
            self.releasegroup_types = '/'.join(types).lower()

        work_id = ''
        if self.mb_workid:
            work_id = self.mb_workid
        else:
            try:
                work_id = recording['work-relation-list'][0]['work']['id']
            except KeyError:
                pass
        if work_id:
            work_hierarchy = work_recursion(work_id, [])
            if work_hierarchy:
                work_hierarchy.reverse()
                self.mb_workid = work_hierarchy[-1]['id']
                self.work = work_hierarchy[-1]['title']
                wh_titles = []
                wh_ids = []
                for work in work_hierarchy:
                    wh_titles.append(work['title'])
                    wh_ids.append(work['id'])
                self.work_hierarchy = ' -> '.join(wh_titles)
                self.mb_workhierarchy_ids = '/'.join(wh_ids)

    def remap_classical(self):
        """Remap some fields to fit better for classical music. For example
        ``composer`` becomes ``artist`` and ``work`` becomes ``album``.
        All overwritten fields are safed in the ``comments`` field. No
        combined properties (like ``composer_safe``) are used and therefore
        some code duplications are done on purpose to avoid circular endless
        loops.
        """
        safe = []

        if self.title:
            safe.append(['title', self.title])
            self.title = re.sub(r'^[^:]*: ?', '', self.title)

            roman = re.findall(r'^([IVXLCDM]*)\.', self.title)
            if roman:
                safe.append(['track', self.track])
                self.track = str(self._roman_to_int(roman[0])).zfill(2)

        if self.composer:
            safe.append(['artist', self.artist])
            self.artist = self.composer

        if self.work:
            safe.append(['album', self.album])
            self.album = self.work

        if safe:
            comments = u'Original metadata: '
            for safed in safe:
                comments = comments + \
                    str(safed[0]) + u': ' + \
                    str(safed[1]) + u'; '

        self.comments = comments

###############################################################################
# Class methods
###############################################################################

    @classmethod
    def fields_phrydy(cls):
        for field in sorted(MediaFile.readable_fields()):
            yield field

    @classmethod
    def fields_audiorename(cls):
        for prop, descriptor in sorted(cls.__dict__.items()):
            if isinstance(getattr(cls, prop), property):
                if isinstance(prop, bytes):
                    # On Python 2, class field names are bytes. This method
                    # produces text strings.
                    yield prop.decode('utf8', 'ignore')
                else:
                    yield prop

    @classmethod
    def fields(cls):
        for field in cls.fields_phrydy():
            yield field
        for field in cls.fields_audiorename():
            yield field

    @classmethod
    def fields_sorted(cls):
        for field in sorted(cls.fields()):
            yield field

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
        if (self.releasegroup_types and
            u'soundtrack' in self.releasegroup_types.lower()) or \
           (self.albumtype and u'soundtrack' in self.albumtype.lower()):
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
    def work_top(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.work_hierarchy``
        * ``phrydy.mediafile.MediaFile.work``

        """
        if self.work_hierarchy:
            return self.work_hierarchy.split(' -> ')[0]
        elif self.album_classical:
            return self.album_classical

    @property
    def year_safe(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.original_year``
        * ``phrydy.mediafile.MediaFile.year``
        """
        if self.original_year:
            return self.original_year
        elif self.year:
            return self.year
