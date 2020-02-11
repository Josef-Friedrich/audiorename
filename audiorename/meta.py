"""Extend the class ``MediaFile`` of the package ``phrydy``.

.. code-block:: Python

    import json
    print(json.dumps(result,indent=2))

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
        "title": "Die Zauberfl\u00f6te: Act I, Scene II. No. 2 Aria ..",
        "artist-relation-list": [
          {
            "type-id": "7474ab81-486f-40b5-8685-3a4f8ea624cb",
            "direction": "backward",
            "type": "librettist",
            "target": "86104c7c-cda4-4798-a4ab-104318c7ae9c",
            "artist": {
              "sort-name": "Schikaneder, Emanuel",
              "id": "86104c7c-cda4-4798-a4ab-104318c7ae9c",
              "name": "Emanuel Schikaneder"
            }
          },
          {
            "begin": "1791",
            "end": "1791",
            "target": "b972f589-fb0e-474e-b64a-803b0364fa75",
            "artist": {
              "sort-name": "Mozart, Wolfgang Amadeus",
              "disambiguation": "classical composer",
              "id": "b972f589-fb0e-474e-b64a-803b0364fa75",
              "name": "Wolfgang Amadeus Mozart"
            },
            "direction": "backward",
            "type-id": "d59d99ea-23d4-4a80-b066-edca32ee158f",
            "ended": "true",
            "type": "composer"
          }
        ]
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

from audiorename._version import get_versions
from phrydy import MediaFile
from tmep import Functions
import musicbrainzngs as mbrainz
import re


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

    if mb_type == 'work':
        mb_includes.append('artist-rels')

    try:
        result = query(mb_id, includes=mb_includes)
        return result[mb_type]

    except mbrainz.ResponseError as err:
        if err.cause.code == 404:
            print('Item of type “' + mb_type + '” with the ID '
                  '“' + mb_id + '” not found.')
        else:
            print("Received bad response from the MusicBrainz server.")


def work_recursion(work_id, works=[]):
    work = query_mbrainz('work', work_id)

    if not work:
        return works

    works.append(work)

    parent_work = False
    if 'work-relation-list' in work:
        for relation in work['work-relation-list']:
            if 'direction' in relation and \
                    relation['direction'] == 'backward' and \
                    relation['type'] == 'parts':
                parent_work = relation
                break

    if parent_work:
        work_recursion(parent_work['work']['id'], works)

    return works


def dict_diff(first, second):
    """Compare two dicts for differenes.

    :param first: Fist dictionary to diff.
    :param second: Second dicationary to diff.
    :return diff: As list of key entries which values differ.
    """
    diff = []
    for key, value in sorted(first.items()):
        if first[key] != second[key]:
            diff.append((key, first[key], second[key]))
    return diff


class Meta(MediaFile):

    def __init__(self, path, shell_friendly=False):
        super(Meta, self).__init__(path, False)
        self.shell_friendly = shell_friendly

###############################################################################
# Public methods
###############################################################################

    def export_dict(self, sanitize=True):
        """
        :param bool sanitize: Boolean value to trigger the sanitize function.
        """
        out = {}
        for field in self.fields_sorted():
            value = getattr(self, field)
            if value:
                if sanitize:
                    out[field] = self._sanitize(str(value))
                else:
                    out[field] = value
            else:
                out[field] = u''

        return out

    def enrich_metadata(self):
        set_useragent()

        if self.mb_trackid:
            recording = query_mbrainz('recording', self.mb_trackid)
        else:
            print('No music brainz track id found.')
            return

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
                work_bottom = work_hierarchy[-1]
                if 'artist-relation-list' in work_bottom:
                    for artist in work_bottom['artist-relation-list']:
                        if artist['direction'] == 'backward' and \
                           artist['type'] == 'composer':
                            self.composer = artist['artist']['name']
                            self.composer_sort = artist['artist']['sort-name']
                            break
                self.mb_workid = work_bottom['id']
                self.work = work_bottom['title']
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
        combined properties (like ``ar_combined_composer``) are used and
        therefore some code duplications are done on purpose to avoid circular
        endless loops.
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

        if self.ar_combined_work_top:
            safe.append(['album', self.album])
            self.ar_performer_short
            album = self.ar_combined_work_top
            if self.ar_performer_short:
                album += ' (' + self.ar_performer_short + ')'
            self.album = album

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
    def _normalize_performer(ar_performer):
        """
        :param list ar_performer: A list of raw ar_performer strings like

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
        if isinstance(ar_performer, list):
            for value in ar_performer:
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
        if isinstance(value, str) or isinstance(value, bytes):
            value = Functions.tmpl_sanitize(value)
            value = re.sub(r'\s{2,}', ' ', value)
        else:
            value = u''
        return value

    @staticmethod
    def _shorten_performer(ar_performer, length=3, separator=u' ',
                           abbreviation=u'.'):
        out = u''
        count = 0
        for s in ar_performer.split(' '):
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
    def ar_classical_album(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.work``

        Examples:

        * ``Horn Concerto: I. Allegro`` → ``Horn Concerto``
        * ``Die Meistersinger von Nürnberg``
        """
        if self.work:
            return re.sub(r':.*$', '', (str(self.work)))
        else:
            return u''

    @property
    def ar_combined_album(self):
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
    def ar_initial_album(self):
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_album`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        return self._initials(self.ar_combined_album)

    @property
    def ar_initial_artist(self):
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_artist_sort`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        return self._initials(self.ar_combined_artist_sort)

    @property
    def ar_combined_artist(self):
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
    def ar_combined_artist_sort(self):
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
        # Same as ar_combined_artist
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
    def ar_initial_composer(self):
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_composer`
        """
        return self._initials(self.ar_combined_composer)

    @property
    def ar_combined_composer(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.composer_sort``
        * ``phrydy.mediafile.MediaFile.composer``
        * :class:`audiorename.meta.Meta.ar_combined_artist`
        """
        if self.composer_sort:
            out = self.composer_sort
        elif self.composer:
            out = self.composer
        else:
            out = self.ar_combined_artist

        if self.shell_friendly:
            out = out.replace(', ', '_')

        # e. g. 'Mozart, Wolfgang Amadeus/Süßmeyer, Franz Xaver'
        return re.sub(r' ?/.*', '', out)

    @property
    def ar_combined_disctrack(self):
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
    def ar_performer(self):
        """Uses:

        * :class:`audiorename.meta.Meta.ar_performer_raw`
        """
        out = u''
        for ar_performer in self.ar_performer_raw:
            out = out + u', ' + ar_performer[1]

        out = out[2:]

        return out

    @property
    def ar_classical_performer(self):
        """http://musicbrainz.org/doc/Style/Classical/Release/Artist

        Uses:

        * :class:`audiorename.meta.Meta.ar_performer_short`
        * ``phrydy.mediafile.MediaFile.albumartist``
        """
        if len(self.ar_performer_short) > 0:
            out = self.ar_performer_short
        elif self.albumartist:
            out = re.sub(r'^.*; ?', '', self.albumartist)
        else:
            out = u''

        return out

    @property
    def ar_performer_raw(self):
        """Generate a unifed ar_performer list.

        Picard doesn’t store ar_performer values in m4a, alac.m4a, wma, wav,
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

            # 4.2.2 TPE3 Conductor/ar_performer refinement
            if len(out) > 0 and 'conductor' not in out[0] \
                    and 'TPE3' in self.mgfile:
                out.insert(0, [u'conductor', self.mgfile['TPE3'].text[0]])

        else:
            out = []

        return self._unify_list(out)

    @property
    def ar_performer_short(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.ar_performer_raw``
        """
        out = []

        performers = self.ar_performer_raw
        picked = []
        for performer in performers:
            if performer[0] == u'conductor' or performer[0] == u'orchestra':
                picked.append(performer)

        if len(picked) > 0:
            performers = picked

        for performer in performers:

            if performer[0] == u'producer' or \
                    performer[0] == u'executive producer' or \
                    performer[0] == 'balance engineer':
                pass
            elif performer[0] == u'orchestra' or \
                    performer[0] == u'choir vocals' or \
                    performer[0] == 'string quartet':
                out.append(self._shorten_performer(performer[1], separator=u'',
                                                   abbreviation=u''))
            else:
                out.append(performer[1].split(' ')[-1])

        return u', '.join(out)

    @property
    def ar_combined_soundtrack(self):
        if (self.releasegroup_types and u'soundtrack'
           in self.releasegroup_types.lower()) or \
           (self.albumtype and u'soundtrack' in self.albumtype.lower()):
            return True
        else:
            return False

    @property
    def ar_classical_title(self):
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
    def ar_classical_track(self):
        """Uses:

        * :class:`audiorename.meta.Meta.ar_classical_title`
        * :class:`audiorename.meta.Meta.ar_combined_disctrack`
        """
        roman = re.findall(r'^([IVXLCDM]*)\.', self.ar_classical_title)
        if roman:
            out = str(self._roman_to_int(roman[0])).zfill(2)
        elif self.ar_combined_disctrack:
            out = self.ar_combined_disctrack
        else:
            out = ''

        return out

    @property
    def ar_combined_work_top(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.work_hierarchy``
        * ``phrydy.mediafile.MediaFile.work``

        """
        if self.work_hierarchy:
            return self.work_hierarchy.split(' -> ')[0]
        elif self.ar_classical_album:
            return self.ar_classical_album

    @property
    def ar_combined_year(self):
        """Uses:

        * ``phrydy.mediafile.MediaFile.original_year``
        * ``phrydy.mediafile.MediaFile.year``
        """
        if self.original_year:
            return self.original_year
        elif self.year:
            return self.year
