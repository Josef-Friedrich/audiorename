# -*- coding: utf-8 -*-

"""Test all metatag fields, the fields from MediaFile too."""

import unittest
import helper

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


class TestYesterday(unittest.TestCase):

    def test_Yesterday(self):
        meta = helper.get_meta(['show-case', 'Beatles_Yesterday.mp3'])

        self.assertEqual(meta.acoustid_fingerprint, None)
        self.assertEqual(meta.acoustid_id, None)
        self.assertEqual(meta.album, u'Help!')
        self.assertEqual(meta.album_classical, u'')
        self.assertEqual(meta.album_clean, u'Help!')
        self.assertEqual(meta.album_initial, u'h')
        self.assertEqual(meta.albumartist, u'The Beatles')
        self.assertEqual(meta.albumartist_credit, None)
        self.assertEqual(meta.albumartist_sort, None)
        self.assertEqual(meta.albumdisambig, None)
        self.assertEqual(meta.albumstatus, u'official')
        self.assertEqual(meta.albumtype, u'album/soundtrack')
        self.assertEqual(meta.arranger, None)
        # self.assertEqual(meta.art, u'')
        # self.assertEqual(meta.artist, u'')
        # self.assertEqual(meta.artist_credit, u'')
        # self.assertEqual(meta.artist_initial, u'')
        # self.assertEqual(meta.artist_sort, u'')
        # self.assertEqual(meta.artistsafe, u'')
        # self.assertEqual(meta.artistsafe_sort, u'')
        # self.assertEqual(meta.asin, u'')
        # self.assertEqual(meta.bitdepth, u'')
        # self.assertEqual(meta.bitrate, u'')
        # self.assertEqual(meta.bpm, u'')
        # self.assertEqual(meta.catalognum, u'')
        # self.assertEqual(meta.channels, u'')
        # self.assertEqual(meta.comments, u'')
        # self.assertEqual(meta.comp, u'')
        # self.assertEqual(meta.composer, u'')
        # self.assertEqual(meta.composer_initial, u'')
        # self.assertEqual(meta.composer_safe, u'')
        # self.assertEqual(meta.composer_sort, u'')
        # self.assertEqual(meta.country, u'')
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
        # self.assertEqual(meta.grouping, u'')
        # self.assertEqual(meta.images, u'')
        # self.assertEqual(meta.initial_key, u'')
        # self.assertEqual(meta.label, u'')
        # self.assertEqual(meta.language, u'')
        # self.assertEqual(meta.length, u'')
        # self.assertEqual(meta.lyricist, u'')
        # self.assertEqual(meta.lyrics, u'')
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
        # self.assertEqual(meta.performer_classical, u'')
        # self.assertEqual(meta.r128_album_gain, u'')
        # self.assertEqual(meta.r128_track_gain, u'')
        # self.assertEqual(meta.rg_album_gain, u'')
        # self.assertEqual(meta.rg_album_peak, u'')
        # self.assertEqual(meta.rg_track_gain, u'')
        # self.assertEqual(meta.rg_track_peak, u'')
        # self.assertEqual(meta.samplerate, u'')
        # self.assertEqual(meta.script, u'')
        # self.assertEqual(meta.title, u'')
        # self.assertEqual(meta.title_classical, u'')
        # self.assertEqual(meta.track, u'')
        # self.assertEqual(meta.track_classical, u'')
        # self.assertEqual(meta.tracktotal, u'')
        # self.assertEqual(meta.work, u'')
        # self.assertEqual(meta.year, u'')
        # self.assertEqual(meta.year_safe, u'')

        # self.assertEqual(meta.acoustid_fingerprint, u'')
        # self.assertEqual(meta.acoustid_id, u'')
        # self.assertEqual(meta.album, u'')
        # self.assertEqual(meta.album_classical, u'')
        # self.assertEqual(meta.album_clean, u'')
        # self.assertEqual(meta.album_initial, u'')
        # self.assertEqual(meta.albumartist, u'')
        # self.assertEqual(meta.albumartist_credit, u'')
        # self.assertEqual(meta.albumartist_sort, u'')
        # self.assertEqual(meta.albumdisambig, u'')
        # self.assertEqual(meta.albumstatus, u'')
        # self.assertEqual(meta.albumtype, u'')
        # self.assertEqual(meta.arranger, u'')
        # self.assertEqual(meta.art, u'')
        # self.assertEqual(meta.artist, u'')
        # self.assertEqual(meta.artist_credit, u'')
        # self.assertEqual(meta.artist_initial, u'')
        # self.assertEqual(meta.artist_sort, u'')
        # self.assertEqual(meta.artistsafe, u'')
        # self.assertEqual(meta.artistsafe_sort, u'')
        # self.assertEqual(meta.asin, u'')
        # self.assertEqual(meta.bitdepth, u'')
        # self.assertEqual(meta.bitrate, u'')
        # self.assertEqual(meta.bpm, u'')
        # self.assertEqual(meta.catalognum, u'')
        # self.assertEqual(meta.channels, u'')
        # self.assertEqual(meta.comments, u'')
        # self.assertEqual(meta.comp, u'')
        # self.assertEqual(meta.composer, u'')
        # self.assertEqual(meta.composer_initial, u'')
        # self.assertEqual(meta.composer_safe, u'')
        # self.assertEqual(meta.composer_sort, u'')
        # self.assertEqual(meta.country, u'')
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
        # self.assertEqual(meta.grouping, u'')
        # self.assertEqual(meta.images, u'')
        # self.assertEqual(meta.initial_key, u'')
        # self.assertEqual(meta.label, u'')
        # self.assertEqual(meta.language, u'')
        # self.assertEqual(meta.length, u'')
        # self.assertEqual(meta.lyricist, u'')
        # self.assertEqual(meta.lyrics, u'')
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
        # self.assertEqual(meta.performer_classical, u'')
        # self.assertEqual(meta.r128_album_gain, u'')
        # self.assertEqual(meta.r128_track_gain, u'')
        # self.assertEqual(meta.rg_album_gain, u'')
        # self.assertEqual(meta.rg_album_peak, u'')
        # self.assertEqual(meta.rg_track_gain, u'')
        # self.assertEqual(meta.rg_track_peak, u'')
        # self.assertEqual(meta.samplerate, u'')
        # self.assertEqual(meta.script, u'')
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
