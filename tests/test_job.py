"""Test the file job.py."""

import typing
from audiorename.job import Job, Timer, Counter
from audiorename.args import ArgsDefault
import unittest
import os
import helper


def job(**kwargs: typing.Any) -> Job:
    return Job(ArgsDefault(**kwargs))


class TestJobWithArgParser(unittest.TestCase):

    ##
    # [selection]
    ##

    def test_source(self):
        self.assertEqual(job(source='.').selection.source,
                         os.path.abspath('.'))

    def test_target_default(self):
        self.assertEqual(job(source='.').selection.target, os.getcwd())

    def test_target(self):
        self.assertEqual(job(target='test').selection.target,
                         os.path.abspath('test'))

    def test_source_as_target(self):
        self.assertEqual(job(source_as_target=True).selection.target,
                         os.getcwd())

    ##
    # [rename]
    ##

    def test_backup_folder(self):
        self.assertEqual(job(backup_folder='/tmp').rename.backup_folder,
                         '/tmp')

    def test_best_format(self):
        self.assertEqual(job(best_format=True).rename.best_format, True)

    def test_dry_run(self):
        self.assertEqual(job(dry_run=True).rename.dry_run, True)

    def test_move_action(self):
        self.assertEqual(job(move_action='copy').rename.move_action, 'copy')

    def test_cleaning_action(self):
        self.assertEqual(
            job(cleaning_action='backup').rename.cleaning_action, 'backup')

    ##
    # [filters]
    ##

    def test_album_complete(self):
        self.assertEqual(job(album_complete=True).filters.album_min, None)
        self.assertEqual(job(album_complete=True).filters.album_complete, True)

    def test_album_min(self):
        self.assertEqual(job(album_min=19).filters.album_min, 19)
        self.assertEqual(job(album_min=19).filters.album_complete, False)

    def test_extension(self):
        self.assertEqual(job(extension='lol').filters.extension, ['lol'])

    def test_field_skip(self):
        self.assertEqual(job(field_skip='album').filters.field_skip, 'album')
    ##
    # [template_settings]
    ##

    def test_shell_friendly(self):
        self.assertEqual(
            job(shell_friendly=True).template_settings.shell_friendly, True)

    ##
    # [cli_output]
    ##

    def test_color(self):
        self.assertEqual(job(color=True).cli_output.color, True)

    def test_debug(self):
        self.assertEqual(job(debug=True).cli_output.debug, True)

    def test_job_info(self):
        self.assertEqual(job(job_info=True).cli_output.job_info, True)

    def test_mb_track_listing(self):
        self.assertEqual(
            job(mb_track_listing=True).cli_output.mb_track_listing, True)

    def test_one_line(self):
        self.assertEqual(job(one_line=True).cli_output.one_line, True)

    def test_stats(self):
        self.assertEqual(job(stats=True).cli_output.stats, True)

    def test_verbose(self):
        self.assertEqual(job(verbose=True).cli_output.verbose, True)

    ##
    # [metadata_actions]
    ##

    def test_enrich_metadata(self):
        self.assertEqual(
            job(enrich_metadata=True).metadata_actions.enrich_metadata, True)

    def test_remap_classical(self):
        self.assertEqual(
            job(remap_classical=True).metadata_actions.remap_classical, True)


def get_config_path(config_file: str) -> str:
    return helper.get_testfile('config', config_file)


def make_job_with_config(config_file: str) -> Job:
    args = ArgsDefault()
    args.config = [get_config_path(config_file)]
    return Job(args)


class TestJobWithConfigParser(unittest.TestCase):

    def setUp(self):
        self.job = make_job_with_config('all-true.ini')

    def test_minimal_config_file(self):
        job = make_job_with_config('minimal.ini')
        self.assertEqual(job.rename.backup_folder, '/tmp/minimal')

    def test_multiple_config_files(self):
        args = ArgsDefault()
        args.config = [
            get_config_path('all-true.ini'),
            get_config_path('minimal.ini'),
        ]
        job = Job(args)
        self.assertEqual(job.rename.backup_folder, '/tmp/minimal')
        self.assertEqual(job.filters.genre_classical, ['sonata', 'opera'])

    def test_multiple_config_file_different_order(self):
        args = ArgsDefault()
        args.config = [
            get_config_path('minimal.ini'),
            get_config_path('all-true.ini'),
        ]
        job = Job(args)
        self.assertEqual(job.rename.backup_folder, '/tmp/backup')

    def test_section_selection(self):
        self.assertEqual(self.job.selection.source, '/tmp')
        self.assertEqual(self.job.selection.target, '/tmp')
        self.assertEqual(self.job.selection.source_as_target, True)

    def test_section_rename(self):
        self.assertEqual(self.job.rename.backup_folder, '/tmp/backup')
        self.assertEqual(self.job.rename.best_format, True)
        self.assertEqual(self.job.rename.dry_run, True)
        self.assertEqual(self.job.rename.move_action, 'copy')
        self.assertEqual(self.job.rename.cleaning_action, 'delete')

    def test_section_filters(self):
        self.assertEqual(self.job.filters.album_complete, True)
        self.assertEqual(self.job.filters.album_min, 42)
        self.assertEqual(self.job.filters.extension, ['wave', 'aiff'])
        self.assertEqual(self.job.filters.genre_classical, ['sonata', 'opera'])
        self.assertEqual(self.job.filters.field_skip, 'comment')

    def test_section_template_settings(self):
        self.assertEqual(self.job.template_settings.classical, True)
        self.assertEqual(self.job.template_settings.shell_friendly, True)
        self.assertEqual(self.job.template_settings.no_soundtrack, True)

    def test_section_path_templates(self):
        self.assertEqual(self.job.path_templates.default, 'classical')
        self.assertEqual(self.job.path_templates.compilation, 'classical')
        self.assertEqual(self.job.path_templates.soundtrack, 'classical')
        self.assertEqual(self.job.path_templates.classical, 'classical')

    def test_section_cli_output(self):
        self.assertEqual(self.job.cli_output.color, True)
        self.assertEqual(self.job.cli_output.debug, True)
        self.assertEqual(self.job.cli_output.job_info, True)
        self.assertEqual(self.job.cli_output.mb_track_listing, True)
        self.assertEqual(self.job.cli_output.one_line, True)
        self.assertEqual(self.job.cli_output.stats, True)
        self.assertEqual(self.job.cli_output.verbose, True)

    def test_section_metadata_actions(self):
        self.assertEqual(self.job.metadata_actions.enrich_metadata, True)
        self.assertEqual(self.job.metadata_actions.remap_classical, True)


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()

    def get_result(self, begin: float, end: float) -> str:
        self.timer.begin = begin
        self.timer.end = end
        return self.timer.result()

    def test_method_start(self):
        self.timer.start()
        self.assertTrue(self.timer.begin > 0)

    def test_method_stop(self):
        self.timer.stop()
        self.assertTrue(self.timer.end > 0)

    def test_method_result(self):
        self.assertEqual(self.get_result(10.3475, 14.594), '4.2s')

    def test_method_result_large(self):
        self.assertEqual(self.get_result(10, 145), '135.0s')

    def test_method_result_small(self):
        self.assertEqual(self.get_result(10.00001, 10.00002), '0.0s')


class TestCounter(unittest.TestCase):

    def setUp(self):
        self.counter = Counter()

    def test_reset(self):
        self.counter.count('lol')
        self.counter.reset()
        self.assertEqual(self.counter.get('lol'), 0)

    def test_count(self):
        self.counter.count('rename')
        self.assertEqual(self.counter.get('rename'), 1)
        self.counter.count('rename')
        self.assertEqual(self.counter.get('rename'), 2)

    def test_result(self):
        self.counter.count('rename')
        self.assertEqual(self.counter.result(),
                         'rename=1')

        self.counter.count('no_field')
        self.assertEqual(self.counter.result(),
                         'no_field=1 rename=1')


if __name__ == '__main__':
    unittest.main()
