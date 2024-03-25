"""Test the file job.py."""

import os
import typing
import unittest

import helper

from audiorename.args import ArgsDefault
from audiorename.job import Counter, Job, Timer


def job(**kwargs: typing.Any) -> Job:
    return Job(ArgsDefault(**kwargs))


class TestJobWithArgParser:
    ##
    # [selection]
    ##

    def test_source(self):
        assert job(source=".").selection.source == os.path.abspath(".")

    def test_target_default(self):
        assert job(source=".").selection.target == os.getcwd()

    def test_target(self):
        assert job(target="test").selection.target == os.path.abspath("test")

    def test_source_as_target(self):
        assert job(source_as_target=True).selection.target == os.getcwd()

    ##
    # [rename]
    ##

    def test_backup_folder(self):
        assert job(backup_folder="/tmp").rename.backup_folder == "/tmp"

    def test_best_format(self):
        assert job(best_format=True).rename.best_format == True

    def test_dry_run(self):
        assert job(dry_run=True).rename.dry_run == True

    def test_move_action(self):
        assert job(move_action="copy").rename.move_action == "copy"

    def test_cleaning_action(self):
        assert job(cleaning_action="backup").rename.cleaning_action == "backup"

    ##
    # [filters]
    ##

    def test_album_complete(self):
        assert job(album_complete=True).filters.album_min == None
        assert job(album_complete=True).filters.album_complete == True

    def test_album_min(self):
        assert job(album_min=19).filters.album_min == 19
        assert job(album_min=19).filters.album_complete == False

    def test_extension(self):
        assert job(extension="lol").filters.extension == ["lol"]

    def test_field_skip(self):
        assert job(field_skip="album").filters.field_skip == "album"

    ##
    # [template_settings]
    ##

    def test_shell_friendly(self):
        assert job(shell_friendly=True).template_settings.shell_friendly == True

    ##
    # [cli_output]
    ##

    def test_color(self):
        assert job(color=True).cli_output.color == True

    def test_debug(self):
        assert job(debug=True).cli_output.debug == True

    def test_job_info(self):
        assert job(job_info=True).cli_output.job_info == True

    def test_mb_track_listing(self):
        assert job(mb_track_listing=True).cli_output.mb_track_listing == True

    def test_one_line(self):
        assert job(one_line=True).cli_output.one_line == True

    def test_stats(self):
        assert job(stats=True).cli_output.stats == True

    def test_verbose(self):
        assert job(verbose=True).cli_output.verbose == True

    ##
    # [metadata_actions]
    ##

    def test_enrich_metadata(self):
        assert job(enrich_metadata=True).metadata_actions.enrich_metadata == True

    def test_remap_classical(self):
        assert job(remap_classical=True).metadata_actions.remap_classical == True


def get_config_path(config_file: str) -> str:
    return helper.get_testfile("config", config_file)


def make_job_with_config(config_file: str) -> Job:
    args = ArgsDefault()
    args.config = [get_config_path(config_file)]
    return Job(args)


class TestJobWithConfigParser:
    def setup_method(self):
        self.job = make_job_with_config("all-true.ini")

    def test_minimal_config_file(self):
        job = make_job_with_config("minimal.ini")
        assert job.rename.backup_folder == "/tmp/minimal"

    def test_multiple_config_files(self):
        args = ArgsDefault()
        args.config = [
            get_config_path("all-true.ini"),
            get_config_path("minimal.ini"),
        ]
        job = Job(args)
        assert job.rename.backup_folder == "/tmp/minimal"
        assert job.filters.genre_classical == ["sonata", "opera"]

    def test_multiple_config_file_different_order(self):
        args = ArgsDefault()
        args.config = [
            get_config_path("minimal.ini"),
            get_config_path("all-true.ini"),
        ]
        job = Job(args)
        assert job.rename.backup_folder == "/tmp/backup"

    def test_section_selection(self):
        assert self.job.selection.source == "/tmp"
        assert self.job.selection.target == "/tmp"
        assert self.job.selection.source_as_target == True

    def test_section_rename(self):
        assert self.job.rename.backup_folder == "/tmp/backup"
        assert self.job.rename.best_format == True
        assert self.job.rename.dry_run == True
        assert self.job.rename.move_action == "copy"
        assert self.job.rename.cleaning_action == "delete"

    def test_section_filters(self):
        assert self.job.filters.album_complete == True
        assert self.job.filters.album_min == 42
        assert self.job.filters.extension == ["wave", "aiff"]
        assert self.job.filters.genre_classical == ["sonata", "opera"]
        assert self.job.filters.field_skip == "comment"

    def test_section_template_settings(self):
        assert self.job.template_settings.classical == True
        assert self.job.template_settings.shell_friendly == True
        assert self.job.template_settings.no_soundtrack == True

    def test_section_path_templates(self):
        assert self.job.path_templates.default == "classical"
        assert self.job.path_templates.compilation == "classical"
        assert self.job.path_templates.soundtrack == "classical"
        assert self.job.path_templates.classical == "classical"

    def test_section_cli_output(self):
        assert self.job.cli_output.color == True
        assert self.job.cli_output.debug == True
        assert self.job.cli_output.job_info == True
        assert self.job.cli_output.mb_track_listing == True
        assert self.job.cli_output.one_line == True
        assert self.job.cli_output.stats == True
        assert self.job.cli_output.verbose == True

    def test_section_metadata_actions(self):
        assert self.job.metadata_actions.enrich_metadata == True
        assert self.job.metadata_actions.remap_classical == True


class TestTimer:
    def setup_method(self):
        self.timer = Timer()

    def get_result(self, begin: float, end: float) -> str:
        self.timer.begin = begin
        self.timer.end = end
        return self.timer.result()

    def test_method_start(self):
        self.timer.start()
        assert self.timer.begin > 0

    def test_method_stop(self):
        self.timer.stop()
        assert self.timer.end > 0

    def test_method_result(self):
        assert self.get_result(10.3475, 14.594) == "4.2s"

    def test_method_result_large(self):
        assert self.get_result(10, 145) == "135.0s"

    def test_method_result_small(self):
        assert self.get_result(10.00001, 10.00002) == "0.0s"


class TestCounter:
    def setup_method(self):
        self.counter = Counter()

    def test_reset(self):
        self.counter.count("lol")
        self.counter.reset()
        assert self.counter.get("lol") == 0

    def test_count(self):
        self.counter.count("rename")
        assert self.counter.get("rename") == 1
        self.counter.count("rename")
        assert self.counter.get("rename") == 2

    def test_result(self):
        self.counter.count("rename")
        assert self.counter.result() == "rename=1"

        self.counter.count("no_field")
        assert self.counter.result() == "no_field=1 rename=1"
