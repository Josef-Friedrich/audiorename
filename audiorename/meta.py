"""Extend the class ``MediaFile`` of the package ``phrydy``.
"""

from phrydy import MediaFileExtended
from tmep import Functions
import re
import typing

import audiorename.musicbrainz as musicbrainz

Diff = typing.List[typing.Tuple[str,
                                typing.Optional[str], typing.Optional[str]]]


def compare_dicts(first: typing.Dict[str, str],
                  second: typing.Dict[str, str]) -> Diff:
    """Compare two dictionaries for differenes.

    :param first: First dictionary to diff.
    :param second: Second dicationary to diff.

    :return: As list of key entries whose values differ.
    """
    diff: Diff = []
    for key, _ in sorted(first.items()):
        if key not in second:
            diff.append((key, first[key], None))

    for key, _ in sorted(second.items()):
        if key not in first:
            diff.append((key, None, second[key]))

    all_keys: set[str] = set()
    for key, _ in first.items():
        all_keys.add(key)
    for key, _ in second.items():
        all_keys.add(key)
    for key in sorted(all_keys):
        if key in first and key in second and first[key] != second[key]:
            diff.append((key, first[key], second[key]))

    return diff


class Meta(MediaFileExtended):

    def __init__(self, path, shell_friendly: bool = False):
        super(Meta, self).__init__(path, False)
        self.shell_friendly = shell_friendly

###############################################################################
# Public methods
###############################################################################

    def export_dict(self, sanitize: bool = True) -> typing.Dict[str, str]:
        """
        Export all fields into a dictionary.

        :param sanitize: Set the parameter to true to trigger the sanitize
          function.
        """
        out = {}
        for field in self.fields_sorted():
            value = getattr(self, field)
            if value:
                if sanitize:
                    out[field] = self._sanitize(str(value))
                else:
                    out[field] = value

        return out

    def enrich_metadata(self) -> None:
        musicbrainz.set_useragent()

        if self.mb_trackid:
            recording = musicbrainz.query('recording', self.mb_trackid)
        else:
            print('No music brainz track id found.')
            return

        release = None
        if self.mb_albumid:
            release = musicbrainz.query('release', self.mb_albumid)
        if release and 'release-group' in release:
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
        elif recording:
            try:
                work_id = recording['work-relation-list'][0]['work']['id']
            except KeyError:
                pass
        if work_id:
            work_hierarchy = musicbrainz.query_works_recursively(work_id, [])
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

    def remap_classical(self) -> None:
        """Remap some fields to fit better for classical music:
        ``composer`` becomes ``artist``, ``work`` becomes ``album``, from the
        ``title`` the work prefix is removed (``Symphonie No. 9: I. Allegro``
        -> ``I. Allegro``) and ``track`` becomes the movement number. All
        overwritten fields are safed in the ``comments`` field. No combined
        properties (like ``ar_combined_composer``) are used and therefore some
        code duplications are done on purpose to avoid circular endless loops.
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
            comments = 'Original metadata: '
            for safed in safe:
                comments = comments + \
                    str(safed[0]) + ': ' + \
                    str(safed[1]) + '; '

            self.comments = comments

###############################################################################
# Class methods
###############################################################################

    @classmethod
    def fields_phrydy(cls):
        for field in sorted(MediaFileExtended.readable_fields()):
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
    def _find_initials(value: str) -> str:
        """
        Find the first character of a string.

        :param str value: A string to extract the initials.

        :return: A single character in lowercase. The possible return values
            are lowercase letters from the ASCII alphabet (``a-z``), the digit
            ``0`` and the underscore character (``_``).
        """
        # To avoid ae -> a
        value = Functions.tmpl_asciify(value)
        # To avoid “!K7-Compilations” -> “!”
        value = re.sub(r'^\W*', '', value)
        initial = value[0:1].lower()

        if re.match(r'\d', initial):
            return '0'

        if initial == '':
            return '_'

        return initial

    @staticmethod
    def _normalize_performer(
            ar_performer: typing.List[str]) -> typing.List[typing.List[str]]:
        """
        :param list ar_performer: A list of raw ar_performer strings like

        .. code-block:: python

            ['John Lennon (vocals)', 'Ringo Starr (drums)']

        :return: A list

        .. code-block:: python

            [
                ['vocals', 'John Lennon'],
                ['drums', 'Ringo Starr'],
            ]
        """
        out = []
        if isinstance(ar_performer, list):
            for value in ar_performer:
                value = value[:-1]
                value = value.split(' (')
                if isinstance(value, list) and len(value) == 2:
                    out.append([value[1], value[0]])
            return out
        else:
            return []

    @staticmethod
    def _roman_to_int(n: str) -> int:
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
    def _sanitize(value) -> str:
        if isinstance(value, str) or isinstance(value, bytes):
            value = Functions.tmpl_sanitize(value)
            value = re.sub(r'\s{2,}', ' ', str(value))
        else:
            value = ''
        return value

    @staticmethod
    def _shorten_performer(ar_performer: str, length: int = 3,
                           separator: str = ' ',
                           abbreviation: str = '.') -> str:
        out = ''
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
    def ar_classical_album(self) -> typing.Optional[str]:
        """Uses:

        * ``phrydy.mediafile.MediaFile.work``

        Examples:

        * ``Horn Concerto: I. Allegro`` → ``Horn Concerto``
        * ``Die Meistersinger von Nürnberg``
        """
        if self.work:
            return re.sub(r':.*$', '', (str(self.work)))

    @property
    def ar_combined_album(self) -> typing.Optional[str]:
        """Uses:

        * ``phrydy.mediafile.MediaFile.album``

        Example:

        * ``Just Friends (Disc 2)`` → ``Just Friends``
        """
        if self.album:
            return re.sub(r' ?\([dD]is[ck].*\)$', '', str(self.album))

    @property
    def ar_initial_album(self) -> typing.Optional[str]:
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_album`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        if self.ar_combined_album:
            return self._find_initials(self.ar_combined_album)

    @property
    def ar_initial_artist(self) -> str:
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_artist_sort`

        Examples:

        * ``Just Friends`` → ``j``
        * ``Die Meistersinger von Nürnberg``  → ``d``
        """
        return self._find_initials(self.ar_combined_artist_sort)

    @property
    def ar_combined_artist(self) -> str:
        """Uses:

        * ``phrydy.mediafile.MediaFile.albumartist``
        * ``phrydy.mediafile.MediaFile.artist``
        * ``phrydy.mediafile.MediaFile.albumartist_credit``
        * ``phrydy.mediafile.MediaFile.artist_credit``
        * ``phrydy.mediafile.MediaFile.albumartist_sort``
        * ``phrydy.mediafile.MediaFile.artist_sort``
        """
        out: str = ''
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
            out = 'Unknown'

        return out

    @property
    def ar_combined_artist_sort(self) -> str:
        """Uses:

        * ``phrydy.mediafile.MediaFile.albumartist_sort``
        * ``phrydy.mediafile.MediaFile.artist_sort``
        * ``phrydy.mediafile.MediaFile.albumartist``
        * ``phrydy.mediafile.MediaFile.artist``
        * ``phrydy.mediafile.MediaFile.albumartist_credit``
        * ``phrydy.mediafile.MediaFile.artist_credit``
        """
        out: str = ''
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
            out = 'Unknown'

        if self.shell_friendly:
            out = out.replace(', ', '_')

        return out

    @property
    def ar_initial_composer(self) -> str:
        """Uses:

        * :class:`audiorename.meta.Meta.ar_combined_composer`
        """
        return self._find_initials(self.ar_combined_composer)

    @property
    def ar_combined_composer(self) -> str:
        """Uses:

        * ``phrydy.mediafile.MediaFile.composer_sort``
        * ``phrydy.mediafile.MediaFile.composer``
        * :class:`audiorename.meta.Meta.ar_combined_artist`
        """
        out: str = ''
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
    def ar_combined_disctrack(self) -> typing.Optional[str]:
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
            return

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
    def ar_performer(self) -> str:
        """Uses:

        * :class:`audiorename.meta.Meta.ar_performer_raw`
        """
        out: str = ''
        for ar_performer in self.ar_performer_raw:
            out = out + ', ' + ar_performer[1]

        out = out[2:]

        return out

    @property
    def ar_classical_performer(self) -> str:
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
            out = ''

        return out

    @property
    def ar_performer_raw(self):
        """Generate a unifed ar_performer list.

        Picard doesn’t store ar_performer values in m4a, alac.m4a, wma, wav,
        aiff.

        :return: A list

        .. code-block:: python

            [
                ['conductor', 'Herbert von Karajan'],
                ['violin', 'Anne-Sophie Mutter'],
            ]

        Uses:

        * ``phrydy.mediafile.MediaFile.mgfile``
        """
        out = []

        if (self.format == 'FLAC' or self.format == 'OGG') and \
                'performer' in self.mgfile:
            out = self._normalize_performer(self.mgfile['performer'])
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

            # 4.2.2 TPE3 Conductor/ar_performer refinement
            if len(out) > 0 and 'conductor' not in out[0] \
                    and 'TPE3' in self.mgfile:
                out.insert(0, ['conductor', self.mgfile['TPE3'].text[0]])

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
            if performer[0] == 'conductor' or performer[0] == 'orchestra':
                picked.append(performer)

        if len(picked) > 0:
            performers = picked

        for performer in performers:

            if performer[0] == 'producer' or \
                    performer[0] == 'executive producer' or \
                    performer[0] == 'balance engineer':
                pass
            elif performer[0] == 'orchestra' or \
                    performer[0] == 'choir vocals' or \
                    performer[0] == 'string quartet':
                out.append(self._shorten_performer(performer[1], separator='',
                                                   abbreviation=''))
            else:
                out.append(performer[1].split(' ')[-1])

        return ', '.join(out)

    @property
    def ar_combined_soundtrack(self):
        if (self.releasegroup_types and 'soundtrack'
            in self.releasegroup_types.lower()) or \
           (self.albumtype and 'soundtrack' in self.albumtype.lower()):
            return True
        else:
            return False

    @property
    def ar_classical_title(self) -> typing.Optional[str]:
        """Uses:

        * ``phrydy.mediafile.MediaFile.title``

        Example:

        * ``Horn Concerto: I. Allegro``
        """
        if self.title:
            return re.sub(r'^[^:]*: ?', '', self.title)

    @property
    def ar_classical_track(self) -> typing.Optional[str]:
        """Uses:

        * :class:`audiorename.meta.Meta.ar_classical_title`
        * :class:`audiorename.meta.Meta.ar_combined_disctrack`
        """
        roman = None
        if self.ar_classical_title:
            roman = re.findall(r'^([IVXLCDM]*)\.', self.ar_classical_title)
        if roman:
            return str(self._roman_to_int(roman[0])).zfill(2)
        elif self.ar_combined_disctrack:
            return self.ar_combined_disctrack

    @property
    def ar_combined_work_top(self) -> typing.Optional[str]:
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
