# -*- coding: utf-8 -*-

"""Test all metatag fields, the fields from MediaFile too."""

import unittest
import helper
import datetime

# from audiorename import args
# from phrydy import doc as pdoc
#
# print(args.all_fields)
#
# for field in sorted(args.all_fields):
#     print(field)

# acoustid_fingerprint
# acoustid_id
# album
# album_classical
# album_clean
# album_initial
# albumartist
# albumartist_credit
# albumartist_sort
# albumdisambig
# albumstatus
# albumtype
# arranger
# art
# artist
# artist_credit
# artist_initial
# artist_sort
# artistsafe
# artistsafe_sort
# asin
# bitdepth
# bitrate
# bpm
# catalognum
# channels
# comments
# comp
# composer
# composer_initial
# composer_safe
# composer_sort
# country
# date
# day
# disc
# disctitle
# disctotal
# disctrack
# encoder
# format
# genre
# genres
# grouping
# images
# initial_key
# label
# language
# length
# lyricist
# lyrics
# mb_albumartistid
# mb_albumid
# mb_artistid
# mb_releasegroupid
# mb_trackid
# mb_workid
# media
# month
# original_date
# original_day
# original_month
# original_year
# performer_classical
# r128_album_gain
# r128_track_gain
# rg_album_gain
# rg_album_peak
# rg_track_gain
# rg_track_peak
# samplerate
# script
# title
# title_classical
# track
# track_classical
# tracktotal
# work
# year
# year_safe


class TestAllFields(unittest.TestCase):

    # Pop-Rock
    def test_Yesterday(self):
        meta = helper.get_meta(['show-case', 'Beatles_Yesterday.mp3'])

        for field in meta.fields_sorted():
            print(field)

        self.assertEqual(meta.acoustid_fingerprint, None)
        self.assertEqual(meta.acoustid_id, None)
        self.assertEqual(meta.album, u'Help!')
        self.assertEqual(meta.album_classical, u'')
        self.assertEqual(meta.album_clean, u'Help!')
        self.assertEqual(meta.album_initial, u'h')
        self.assertEqual(meta.albumartist, u'The Beatles')
        self.assertEqual(meta.albumartist_credit, None)
        self.assertEqual(meta.albumartist_sort, u'Beatles, The')
        self.assertEqual(meta.albumdisambig, None)
        self.assertEqual(meta.albumstatus, u'official')
        self.assertEqual(meta.albumtype, u'album/soundtrack')
        self.assertEqual(meta.arranger, None)
        # self.assertEqual(meta.art, u'')
        self.assertEqual(meta.artist, u'The Beatles')
        self.assertEqual(meta.artist_credit, None)
        self.assertEqual(meta.artist_initial, u'b')
        self.assertEqual(meta.artist_sort, u'Beatles, The')
        self.assertEqual(meta.artistsafe, u'The Beatles')
        self.assertEqual(meta.artistsafe_sort, u'Beatles, The')
        self.assertEqual(meta.asin, u'B000002UAL')
        self.assertEqual(meta.bitdepth, 0)
        self.assertEqual(meta.bitrate, 8000)
        self.assertEqual(meta.bpm, None)
        self.assertEqual(meta.catalognum, u'CDP 7 46439 2')
        self.assertEqual(meta.channels, 1)
        self.assertEqual(meta.comments, None)
        self.assertEqual(meta.comp, None)
        self.assertEqual(meta.composer, None)
        # should b
        self.assertEqual(meta.composer_initial, u't')
        self.assertEqual(meta.composer_safe, u'The Beatles')
        self.assertEqual(meta.composer_sort, None)
        self.assertEqual(meta.country, u'GB')
        self.assertEqual(meta.date, datetime.date(1987, 4, 30))
        self.assertEqual(meta.day, 30)
        self.assertEqual(meta.disc, 1)
        self.assertEqual(meta.disctitle, None)
        self.assertEqual(meta.disctotal, 1)
        # int
        self.assertEqual(meta.disctrack, '13')
        self.assertEqual(meta.encoder, None)
        self.assertEqual(meta.format, u'MP3')
        self.assertEqual(meta.genre, None)
        self.assertEqual(meta.genres, [])
        self.assertEqual(meta.grouping, None)
        # [<phrydy.mediafile.Image object at 0x7f93fa63d510>]
        # self.assertEqual(meta.images, u'')
        self.assertEqual(meta.initial_key, None)
        self.assertEqual(meta.label, u'Parlophone')
        self.assertEqual(meta.language, None)
        self.assertEqual(meta.length, 0.296)
        self.assertEqual(meta.lyricist, None)
        self.assertEqual(meta.lyrics, None)
        self.assertEqual(meta.mb_albumartistid,
                         u'b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d')
        self.assertEqual(meta.mb_albumid,
                         u'95e9dc60-a6d9-315f-be99-bd5b69a6582f')
        self.assertEqual(meta.mb_artistid,
                         u'b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d')
        self.assertEqual(meta.mb_releasegroupid,
                         u'0d44e1cb-c6e0-3453-8b68-4d2082f05421')
        self.assertEqual(meta.mb_trackid,
                         u'c05194a3-f6f0-4f52-b78a-13fb5580bc0f')
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.media, u'CD')
        self.assertEqual(meta.month, 4)
        self.assertEqual(meta.original_date, datetime.date(1965, 1, 1))
        self.assertEqual(meta.original_day, None)
        self.assertEqual(meta.original_month, None)
        self.assertEqual(meta.original_year, 1965)
        self.assertEqual(meta.performer_classical, u'The Beatles')
        self.assertEqual(meta.r128_album_gain, None)
        self.assertEqual(meta.r128_track_gain, None)
        self.assertEqual(meta.rg_album_gain, None)
        self.assertEqual(meta.rg_album_peak, None)
        self.assertEqual(meta.rg_track_gain, None)
        self.assertEqual(meta.rg_track_peak, None)
        self.assertEqual(meta.samplerate, 24000)
        self.assertEqual(meta.soundtrack, True)
        self.assertEqual(meta.script, u'Latn')
        self.assertEqual(meta.title, u'Yesterday')
        self.assertEqual(meta.title_classical, u'Yesterday')
        self.assertEqual(meta.track, 13)
        #  int
        self.assertEqual(meta.track_classical, '13')
        self.assertEqual(meta.tracktotal, 14)
        self.assertEqual(meta.work, None)
        self.assertEqual(meta.year, 1987)
        # int
        self.assertEqual(meta.year_safe, '1965')

    # Classical
    def test_Nachtmusik(self):
        meta = helper.get_meta(['show-case', 'Mozart_Nachtmusik.mp3'])

        self.assertEqual(meta.acoustid_fingerprint, None)
        self.assertEqual(meta.acoustid_id, None)
        self.assertEqual(meta.album, u'Divertimenti')
        self.assertEqual(meta.album_classical, u'')
        self.assertEqual(meta.album_clean, u'Divertimenti')
        self.assertEqual(meta.album_initial, u'd')
        self.assertEqual(meta.albumartist,
                         u'Wolfgang Amadeus Mozart; Berliner ' +
                         'Philharmoniker, Herbert von Karajan')
        self.assertEqual(meta.albumartist_credit, None)
        self.assertEqual(meta.albumartist_sort, u'Mozart, Wolfgang Amadeus; '
                         'Berliner Philharmoniker, Karajan, Herbert von')
        self.assertEqual(meta.albumdisambig, None)
        self.assertEqual(meta.albumstatus, u'official')
        self.assertEqual(meta.albumtype, u'album')
        self.assertEqual(meta.arranger, None)
        # self.assertEqual(meta.art, u'')
        self.assertEqual(meta.artist, u'Wolfgang Amadeus Mozart')
        self.assertEqual(meta.artist_credit, None)
        self.assertEqual(meta.artist_initial, u'm')
        self.assertEqual(meta.artist_sort, u'Mozart, Wolfgang Amadeus')
        self.assertEqual(meta.artistsafe,
                         u'Wolfgang Amadeus Mozart; Berliner ' +
                         'Philharmoniker, Herbert von Karajan')
        self.assertEqual(meta.artistsafe_sort, u'Mozart, Wolfgang Amadeus; '
                         'Berliner Philharmoniker, Karajan, Herbert von')
        self.assertEqual(meta.asin, u'B0007DHPQ2')
        self.assertEqual(meta.bitdepth, 0)
        self.assertEqual(meta.bitrate, 8000)
        self.assertEqual(meta.bpm, None)
        self.assertEqual(meta.catalognum, u'477 5436')
        self.assertEqual(meta.channels, 1)
        self.assertEqual(meta.comments, None)
        self.assertEqual(meta.comp, None)
        self.assertEqual(meta.composer, None)
        self.assertEqual(meta.composer_initial, u'w')
        self.assertEqual(meta.composer_safe,
                         u'Wolfgang Amadeus Mozart; Berliner ' +
                         'Philharmoniker, Herbert von Karajan')
        self.assertEqual(meta.composer_sort, None)
        self.assertEqual(meta.country, u'DE')
        self.assertEqual(meta.date, datetime.date(2005, 3, 10))
        self.assertEqual(meta.day, 10)
        self.assertEqual(meta.disc, 1)
        self.assertEqual(meta.disctitle, None)
        self.assertEqual(meta.disctotal, 2)
        self.assertEqual(meta.disctrack, u'1-01')
        self.assertEqual(meta.encoder, None)
        self.assertEqual(meta.format, u'MP3')
        self.assertEqual(meta.genre, None)
        self.assertEqual(meta.genres, [])
        self.assertEqual(meta.grouping, None)
        # self.assertEqual(meta.images, u'')
        self.assertEqual(meta.initial_key, None)
        self.assertEqual(meta.label, u'Deutsche Grammophon')
        self.assertEqual(meta.language, None)
        self.assertEqual(meta.length, 0.296)
        self.assertEqual(meta.lyricist, None)
        self.assertEqual(meta.lyrics, None)
        self.assertEqual(meta.mb_albumartistid,
                         u'b972f589-fb0e-474e-b64a-803b0364fa75/' +
                         'dea28aa9-1086-4ffa-8739-0ccc759de1ce/' +
                         'd2ced2f1-6b58-47cf-ae87-5943e2ab6d99')
        self.assertEqual(meta.mb_albumid,
                         u'73678131-46a7-442b-8cce-27a8b3bf99c7')
        self.assertEqual(meta.mb_artistid,
                         u'b972f589-fb0e-474e-b64a-803b0364fa75')
        self.assertEqual(meta.mb_releasegroupid,
                         u'17267766-771b-45fe-969f-14b9c4b15e4a')
        self.assertEqual(meta.mb_trackid,
                         u'0db2cdc3-8272-44ef-9810-c75c3939ece8')
        self.assertEqual(meta.mb_workid, None)
        self.assertEqual(meta.media, u'CD')
        self.assertEqual(meta.month, 3)
        self.assertEqual(meta.original_date, datetime.date(2005, 1, 1))
        self.assertEqual(meta.original_day, None)
        self.assertEqual(meta.original_month, None)
        self.assertEqual(meta.original_year, 2005)
        self.assertEqual(meta.performer_classical,
                         u'Berliner Philharmoniker, Herbert von Karajan')
        self.assertEqual(meta.r128_album_gain, None)
        self.assertEqual(meta.r128_track_gain, None)
        self.assertEqual(meta.rg_album_gain, None)
        self.assertEqual(meta.rg_album_peak, None)
        self.assertEqual(meta.rg_track_gain, None)
        self.assertEqual(meta.rg_track_peak, None)
        self.assertEqual(meta.samplerate, 24000)
        self.assertEqual(meta.script, u'Latn')
        self.assertEqual(meta.soundtrack, False)
        self.assertEqual(meta.title,
                         u'Serenade no. 13 for Strings in G major, K. 525 ' +
                         '"Eine kleine Nachtmusik": I. Allegro')
        self.assertEqual(meta.title_classical, u'I. Allegro')
        self.assertEqual(meta.track, 1)
        self.assertEqual(meta.track_classical, u'01')
        self.assertEqual(meta.tracktotal, 16)
        self.assertEqual(meta.work, None)
        self.assertEqual(meta.year, 2005)
        self.assertEqual(meta.year_safe, u'2005')

    # Jazz
    def test_Wonderful(self):
        meta = helper.get_meta(['show-case', 'Armstrong_Wonderful-World.mp3'])
        self.assertEqual(meta.acoustid_fingerprint, None)
        self.assertEqual(meta.acoustid_id, None)
        self.assertEqual(meta.album, u'Greatest Hits')
        self.assertEqual(meta.album_classical, u'')
        self.assertEqual(meta.album_clean, u'Greatest Hits')
        self.assertEqual(meta.album_initial, u'g')
        self.assertEqual(meta.albumartist, u'Louis Armstrong')
        self.assertEqual(meta.albumartist_credit, None)
        self.assertEqual(meta.albumartist_sort, u'Armstrong, Louis')
        self.assertEqual(meta.albumdisambig, None)
        self.assertEqual(meta.albumstatus, u'official')
        self.assertEqual(meta.albumtype, u'album/compilation')
        self.assertEqual(meta.arranger, None)
        # self.assertEqual(meta.art, u'')
        self.assertEqual(meta.artist, u'Louis Armstrong')
        self.assertEqual(meta.artist_credit, None)
        self.assertEqual(meta.artist_initial, u'a')
        self.assertEqual(meta.artist_sort, u'Armstrong, Louis')
        self.assertEqual(meta.artistsafe, u'Louis Armstrong')
        self.assertEqual(meta.artistsafe_sort, u'Armstrong, Louis')
        self.assertEqual(meta.asin, u'B000003G2C')
        self.assertEqual(meta.bitdepth, 0)
        self.assertEqual(meta.bitrate, 8000)
        self.assertEqual(meta.bpm, None)
        self.assertEqual(meta.catalognum, u'09026-68486-2')
        self.assertEqual(meta.channels, 1)
        self.assertEqual(meta.comments, None)
        self.assertEqual(meta.comp, None)
        self.assertEqual(meta.composer, None)
        self.assertEqual(meta.composer_initial, u'l')
        self.assertEqual(meta.composer_safe, u'Louis Armstrong')
        self.assertEqual(meta.composer_sort, None)
        self.assertEqual(meta.country, u'US')
        # self.assertEqual(meta.date, u'')
        # self.assertEqual(meta.day, u'')
        # self.assertEqual(meta.disc, u'')
        # self.assertEqual(meta.disctitle, u'')
        # self.assertEqual(meta.disctotal, u'')
        # self.assertEqual(meta.disctrack, u'')
        # self.assertEqual(meta.encoder, u'')
        # self.assertEqual(meta.format, u'')
        # self.assertEqual(meta.genre, u'')
        # self.assertEqual(meta.genres, u'')
        self.assertEqual(meta.grouping, None)
        # self.assertEqual(meta.images, u'')
        self.assertEqual(meta.initial_key, None)
        # self.assertEqual(meta.label, u'')
        # self.assertEqual(meta.language, u'')
        # self.assertEqual(meta.length, u'')
        self.assertEqual(meta.lyricist, None)
        self.assertEqual(meta.lyrics, None)
        # self.assertEqual(meta.mb_albumartistid, u'')
        # self.assertEqual(meta.mb_albumid, u'')
        # self.assertEqual(meta.mb_artistid, u'')
        # self.assertEqual(meta.mb_releasegroupid, u'')
        # self.assertEqual(meta.mb_trackid, u'')
        # self.assertEqual(meta.mb_workid, u'')
        # self.assertEqual(meta.media, u'')
        # self.assertEqual(meta.month, u'')
        # self.assertEqual(meta.original_date, u'')
        # self.assertEqual(meta.original_day, u'')
        # self.assertEqual(meta.original_month, u'')
        # self.assertEqual(meta.original_year, u'')
        self.assertEqual(meta.performer_classical, u'Louis Armstrong')
        self.assertEqual(meta.r128_album_gain, None)
        self.assertEqual(meta.r128_track_gain, None)
        self.assertEqual(meta.rg_album_gain, None)
        self.assertEqual(meta.rg_album_peak, None)
        self.assertEqual(meta.rg_track_gain, None)
        self.assertEqual(meta.rg_track_peak, None)
        self.assertEqual(meta.samplerate, 24000)
        self.assertEqual(meta.script, u'Latn')
        self.assertEqual(meta.soundtrack, False)
        # self.assertEqual(meta.title, u'')
        # self.assertEqual(meta.title_classical, u'')
        # self.assertEqual(meta.track, u'')
        # self.assertEqual(meta.track_classical, u'')
        # self.assertEqual(meta.tracktotal, u'')
        # self.assertEqual(meta.work, u'')
        # self.assertEqual(meta.year, u'')
        # self.assertEqual(meta.year_safe, u'')


if __name__ == '__main__':
    unittest.main()
