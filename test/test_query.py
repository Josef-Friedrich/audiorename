# -*- coding: utf-8 -*-

import unittest
from audiorename.query import get_work, read, save
import os
import tempfile
import shutil

test_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'classical',
    'without_work.mp3'
)


class TestQuery(unittest.TestCase):

    # test/classical/Wagner_Meistersinger/01.mp3
    #
    # mb_trackid:
    #   00ba1660-4e35-4985-86b2-8b7a3e99b1e5
    #
    # mb_workid:
    #   6b198406-4fbf-3d61-82db-0b7ef195a7fe
    #
    # work:
    #   Die Meistersinger von Nürnberg: Akt I. Vorspiel
    def test_query(self):
        result = get_work('00ba1660-4e35-4985-86b2-8b7a3e99b1e5')
        work = result['recording']['work-relation-list'][0]
        self.assertEqual(work['work']['id'],
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')
        self.assertTrue(work['work']['title'])

    def test_read(self):
        result = read(test_file)
        self.assertEqual(result.mb_trackid,
                         '00ba1660-4e35-4985-86b2-8b7a3e99b1e5')

    def test_save(self):
        tmp_file = tempfile.mktemp()
        shutil.copy2(test_file, tmp_file)
        result = save(tmp_file)
        self.assertEqual(result.mb_workid,
                         '6b198406-4fbf-3d61-82db-0b7ef195a7fe')


if __name__ == '__main__':
    unittest.main()
