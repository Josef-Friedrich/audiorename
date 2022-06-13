from audiorename.musicbrainz import \
    query, query_works_recursively, set_useragent

import unittest

import helper


class TestEnrich(unittest.TestCase):

    def setUp(self):
        set_useragent()

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_recording_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = query(
            'recording',
            '0480672d-4d88-4824-a06b-917ff408eabe',
        )
        self.assertEqual(result['id'],
                         '0480672d-4d88-4824-a06b-917ff408eabe')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_recording_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3']
        result = query(
            'recording',
            '7886ad6c-11af-435b-8ec3-bca5711f7728',
        )
        self.assertEqual(result['work-relation-list'][0]['work']['id'],
                         '21fe0bf0-a040-387c-a39d-369d53c251fe')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_release_pulp_01(self):
        # ['soundtrack', 'Pulp-Fiction', '01.mp3']
        result = query(
            'release',
            'ab81edcb-9525-47cd-8247-db4fa969f525',
        )
        self.assertEqual(result['release-group']['id'],
                         '1703cd63-9401-33c0-87c6-50c4ba2e0ba8')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_release_mozart_01(self):
        # ['classical', 'Mozart_Horn-concertos', '01.mp3'])
        result = query(
            'release',
            '5ed650c5-0f72-4b79-80a7-c458c869f53e',
        )
        self.assertEqual(result['release-group']['id'],
                         'e1fa28f0-e56e-395b-82d3-a8de54e8c627')

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_work_mozart_zauberfloete_unit(self):
        # recording_id 6a0599ea-5c06-483a-ba66-f3a036da900a
        # work_id eafec51f-47c5-3c66-8c36-a524246c85f8
        # Akt 1: 5adc213f-700a-4435-9e95-831ed720f348
        result = query_works_recursively(
            'eafec51f-47c5-3c66-8c36-a524246c85f8', [])

        self.assertEqual(result[0]['id'],
                         'eafec51f-47c5-3c66-8c36-a524246c85f8')
        self.assertEqual(result[1]['id'],
                         '5adc213f-700a-4435-9e95-831ed720f348')
        self.assertEqual(result[2]['id'],
                         'e208c5f5-5d37-3dfc-ac0b-999f207c9e46')
        self.assertTrue('artist-relation-list' in result[2])

    @unittest.skipIf(helper.SKIP_API_CALLS, 'Disable if API not available')
    def test_work_kempff_transcription(self):
        # work_id 4fba670e-3b8e-4ddf-a3a6-90817c94d6ce
        result = query_works_recursively(
            '4fba670e-3b8e-4ddf-a3a6-90817c94d6ce', [])
        self.assertEqual(result[0]['id'],
                         '4fba670e-3b8e-4ddf-a3a6-90817c94d6ce')
        self.assertEqual(len(result), 1)