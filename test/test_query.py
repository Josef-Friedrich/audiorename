# -*- coding: utf-8 -*-

import unittest
from audiorename.query import get_work


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
        self.assertEqual(
            work['work']['title'],
            u'Die Meistersinger von Nürnberg, WWV 96: Akt I. Vorspiel'
        )


if __name__ == '__main__':
    unittest.main()
