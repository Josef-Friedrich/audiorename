"""Test all metatag fields, the fields from MediaFile too."""

import datetime

from tests import helper

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
# ar_classical_album
# ar_combined_album
# ar_initial_album
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
# ar_initial_artist
# artist_sort
# ar_combined_artist
# ar_combined_artist_sort
# asin
# bitdepth
# bitrate
# bpm
# catalognum
# channels
# comments
# comp
# composer
# ar_initial_composer
# ar_combined_composer
# composer_sort
# country
# date
# day
# disc
# disctitle
# disctotal
# ar_combined_disctrack
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
# ar_classical_performer
# r128_album_gain
# r128_track_gain
# rg_album_gain
# rg_album_peak
# rg_track_gain
# rg_track_peak
# samplerate
# script
# title
# ar_classical_title
# track
# ar_classical_track
# tracktotal
# work
# year
# ar_combined_year


class TestAllFields:
    # Pop-Rock
    def test_yesterday(self):
        meta = helper.get_meta("show-case", "Beatles_Yesterday.mp3")

        assert meta.acoustid_fingerprint is None
        assert meta.acoustid_id is None
        assert meta.album == "Help!"
        assert meta.ar_classical_album is None
        assert meta.ar_combined_album == "Help!"
        assert meta.ar_initial_album == "h"
        assert meta.albumartist == "The Beatles"
        assert meta.albumartist_credit is None
        assert meta.albumartist_sort == "Beatles, The"
        assert meta.albumdisambig is None
        assert meta.albumstatus == "official"
        assert meta.albumtype == "album"
        assert meta.arranger is None
        # self.assertEqual(meta.art, '')
        assert meta.artist == "The Beatles"
        assert meta.artist_credit is None
        assert meta.ar_initial_artist == "b"
        assert meta.artist_sort == "Beatles, The"
        assert meta.ar_combined_artist == "The Beatles"
        assert meta.ar_combined_artist_sort == "Beatles, The"
        assert meta.asin == "B000002UAL"
        assert meta.bitdepth == 0
        assert meta.bitrate == 8000
        assert meta.bpm is None
        assert meta.catalognum == "CDP 7 46439 2"
        assert meta.channels == 1
        assert meta.comments is None
        assert meta.comp is None
        assert meta.composer is None
        # should b
        assert meta.ar_initial_composer == "t"
        assert meta.ar_combined_composer == "The Beatles"
        assert meta.composer_sort is None
        assert meta.country == "GB"
        assert meta.date == datetime.date(1987, 4, 30)
        assert meta.day == 30
        assert meta.disc == 1
        assert meta.disctitle is None
        assert meta.disctotal == 1
        # int
        assert meta.ar_combined_disctrack == "13"
        assert meta.encoder is None
        assert meta.format == "MP3"
        assert meta.genre is None
        assert meta.genres is None
        assert meta.grouping is None
        # self.assertTrue(isinstance(meta.images[0],
        # phrydy.mediafile_extended.Image))
        assert meta.initial_key is None
        assert meta.label == "Parlophone"
        assert meta.language is None
        assert meta.length == 0.296
        assert meta.lyricist is None
        assert meta.lyrics is None
        assert meta.mb_albumartistid == "b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d"
        assert meta.mb_albumid == "95e9dc60-a6d9-315f-be99-bd5b69a6582f"
        assert meta.mb_artistid == "b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d"
        assert meta.mb_releasegroupid == "0d44e1cb-c6e0-3453-8b68-4d2082f05421"
        assert meta.mb_trackid == "c05194a3-f6f0-4f52-b78a-13fb5580bc0f"
        assert meta.mb_workid is None
        assert meta.media == "CD"
        assert meta.month == 4
        assert meta.original_date == datetime.date(1965, 1, 1)
        assert meta.original_day is None
        assert meta.original_month is None
        assert meta.original_year == 1965
        assert meta.ar_classical_performer == "The Beatles"
        assert meta.r128_album_gain is None
        assert meta.r128_track_gain is None
        assert meta.rg_album_gain is None
        assert meta.rg_album_peak is None
        assert meta.rg_track_gain is None
        assert meta.rg_track_peak is None
        assert meta.samplerate == 24000
        assert meta.ar_combined_soundtrack is True
        assert meta.script == "Latn"
        assert meta.title == "Yesterday"
        assert meta.ar_classical_title == "Yesterday"
        assert meta.track == 13
        #  int
        assert meta.ar_classical_track == "13"
        assert meta.tracktotal == 14
        assert meta.work is None
        assert meta.year == 1987
        # int
        assert meta.ar_combined_year == 1965

    # Classical
    def test_nachtmusik(self):
        meta = helper.get_meta("show-case", "Mozart_Nachtmusik.mp3")

        assert meta.acoustid_fingerprint is None
        assert meta.acoustid_id is None
        assert meta.album == "Divertimenti"
        assert meta.ar_classical_album is None
        assert meta.ar_combined_album == "Divertimenti"
        assert meta.ar_initial_album == "d"
        assert (
            meta.albumartist == "Wolfgang Amadeus Mozart; Berliner "
            "Philharmoniker, Herbert von Karajan"
        )
        assert meta.albumartist_credit is None
        assert (
            meta.albumartist_sort == "Mozart, Wolfgang Amadeus; "
            "Berliner Philharmoniker, Karajan, Herbert von"
        )
        assert meta.albumdisambig is None
        assert meta.albumstatus == "official"
        assert meta.albumtype == "album"
        assert meta.arranger is None
        # self.assertEqual(meta.art, '')
        assert meta.artist == "Wolfgang Amadeus Mozart"
        assert meta.artist_credit is None
        assert meta.ar_initial_artist == "m"
        assert meta.artist_sort == "Mozart, Wolfgang Amadeus"
        assert (
            meta.ar_combined_artist == "Wolfgang Amadeus Mozart; Berliner "
            "Philharmoniker, Herbert von Karajan"
        )
        assert (
            meta.ar_combined_artist_sort == "Mozart, Wolfgang Amadeus; "
            "Berliner Philharmoniker, Karajan, Herbert von"
        )
        assert meta.asin == "B0007DHPQ2"
        assert meta.bitdepth == 0
        assert meta.bitrate == 8000
        assert meta.bpm is None
        assert meta.catalognum == "477 5436"
        assert meta.channels == 1
        assert meta.comments is None
        assert meta.comp is None
        assert meta.composer is None
        assert meta.ar_initial_composer == "w"
        assert (
            meta.ar_combined_composer == "Wolfgang Amadeus Mozart; Berliner "
            "Philharmoniker, Herbert von Karajan"
        )
        assert meta.composer_sort is None
        assert meta.country == "DE"
        assert meta.date == datetime.date(2005, 3, 10)
        assert meta.day == 10
        assert meta.disc == 1
        assert meta.disctitle is None
        assert meta.disctotal == 2
        assert meta.ar_combined_disctrack == "1-01"
        assert meta.encoder is None
        assert meta.format == "MP3"
        assert meta.genre is None
        assert meta.genres is None
        assert meta.grouping is None
        # self.assertTrue(isinstance(meta.images[0], phrydy.mediafile.Image))
        assert meta.initial_key is None
        assert meta.label == "Deutsche Grammophon"
        assert meta.language is None
        assert meta.length == 0.296
        assert meta.lyricist is None
        assert meta.lyrics is None
        assert meta.mb_albumartistid == "b972f589-fb0e-474e-b64a-803b0364fa75"
        assert meta.mb_albumartistids == [
            "b972f589-fb0e-474e-b64a-803b0364fa75",
            "dea28aa9-1086-4ffa-8739-0ccc759de1ce",
            "d2ced2f1-6b58-47cf-ae87-5943e2ab6d99",
        ]
        assert meta.mb_albumid == "73678131-46a7-442b-8cce-27a8b3bf99c7"
        assert meta.mb_artistid == "b972f589-fb0e-474e-b64a-803b0364fa75"
        assert meta.mb_releasegroupid == "17267766-771b-45fe-969f-14b9c4b15e4a"
        assert meta.mb_trackid == "0db2cdc3-8272-44ef-9810-c75c3939ece8"
        assert meta.mb_workid is None
        assert meta.media == "CD"
        assert meta.month == 3
        assert meta.original_date == datetime.date(2005, 1, 1)
        assert meta.original_day is None
        assert meta.original_month is None
        assert meta.original_year == 2005
        assert (
            meta.ar_classical_performer
            == "Berliner Philharmoniker, Herbert von Karajan"
        )
        assert meta.r128_album_gain is None
        assert meta.r128_track_gain is None
        assert meta.rg_album_gain is None
        assert meta.rg_album_peak is None
        assert meta.rg_track_gain is None
        assert meta.rg_track_peak is None
        assert meta.samplerate == 24000
        assert meta.script == "Latn"
        assert meta.ar_combined_soundtrack == False
        assert (
            meta.title == "Serenade no. 13 for Strings in G major, K. 525 "
            '"Eine kleine Nachtmusik": I. Allegro'
        )
        assert meta.ar_classical_title == "I. Allegro"
        assert meta.track == 1
        assert meta.ar_classical_track == "01"
        assert meta.tracktotal == 16
        assert meta.work is None
        assert meta.year == 2005
        assert meta.ar_combined_year == 2005

    # Jazz
    def test_wonderful(self):
        meta = helper.get_meta("show-case", "Armstrong_Wonderful-World.mp3")
        assert meta.acoustid_fingerprint is None
        assert meta.acoustid_id is None
        assert meta.album == "Greatest Hits"
        assert meta.ar_classical_album is None
        assert meta.ar_combined_album == "Greatest Hits"
        assert meta.ar_initial_album == "g"
        assert meta.albumartist == "Louis Armstrong"
        assert meta.albumartist_credit is None
        assert meta.albumartist_sort == "Armstrong, Louis"
        assert meta.albumdisambig is None
        assert meta.albumstatus == "official"
        assert meta.albumtype == "album"
        assert meta.arranger is None
        # self.assertEqual(meta.art, '')
        assert meta.artist == "Louis Armstrong"
        assert meta.artist_credit is None
        assert meta.ar_initial_artist == "a"
        assert meta.artist_sort == "Armstrong, Louis"
        assert meta.ar_combined_artist == "Louis Armstrong"
        assert meta.ar_combined_artist_sort == "Armstrong, Louis"
        assert meta.asin == "B000003G2C"
        assert meta.bitdepth == 0
        assert meta.bitrate == 8000
        assert meta.bpm is None
        assert meta.catalognum == "09026-68486-2"
        assert meta.channels == 1
        assert meta.comments is None
        assert meta.comp is None
        assert meta.composer is None
        assert meta.ar_initial_composer == "l"
        assert meta.ar_combined_composer == "Louis Armstrong"
        assert meta.composer_sort is None
        assert meta.country == "US"
        assert meta.date == datetime.date(1996, 1, 1)
        assert meta.day is None
        assert meta.disc == 1
        assert meta.disctitle is None
        assert meta.disctotal == 1
        assert meta.ar_combined_disctrack == "13"
        assert meta.encoder is None
        assert meta.format == "MP3"
        assert meta.genre is None
        assert meta.genres is None
        assert meta.grouping is None
        # self.assertTrue(isinstance(meta.images[0], phrydy.mediafile.Image))
        assert meta.initial_key is None
        # self.assertEqual(meta.label, '')
        # self.assertEqual(meta.language, '')
        # self.assertEqual(meta.length, '')
        assert meta.lyricist is None
        assert meta.lyrics is None
        # self.assertEqual(meta.mb_albumartistid, '')
        # self.assertEqual(meta.mb_albumid, '')
        # self.assertEqual(meta.mb_artistid, '')
        # self.assertEqual(meta.mb_releasegroupid, '')
        # self.assertEqual(meta.mb_trackid, '')
        # self.assertEqual(meta.mb_workid, '')
        # self.assertEqual(meta.media, '')
        assert meta.month is None
        assert meta.original_date == datetime.date(1996, 1, 1)
        assert meta.original_day is None
        assert meta.original_month is None
        assert meta.original_year == 1996
        assert meta.ar_classical_performer == "Louis Armstrong"
        assert meta.r128_album_gain is None
        assert meta.r128_track_gain is None
        assert meta.rg_album_gain is None
        assert meta.rg_album_peak is None
        assert meta.rg_track_gain is None
        assert meta.rg_track_peak is None
        assert meta.samplerate == 24000
        assert meta.script == "Latn"
        assert meta.ar_combined_soundtrack == False
        assert meta.title == "What a Wonderful World"
        assert meta.ar_classical_title == "What a Wonderful World"
        assert meta.track == 13
        assert meta.ar_classical_track == "13"
        assert meta.tracktotal == 13
        assert meta.work is None
        assert meta.year == 1996
        assert meta.ar_combined_year == 1996
