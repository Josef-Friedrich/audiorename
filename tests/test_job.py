"""Test the file job.py."""

import os
import typing

import helper

from audiorename.args import ArgsDefault
from audiorename.job import Counter, Job, Timer


def job(**kwargs: typing.Any) -> Job:
    return Job(ArgsDefault(**kwargs))


class TestJobWithArgParser:
    ##
    # [selection]
    ##

    def test_source(self) -> None:
        assert job(source=".").selection.source == os.path.abspath(".")

    def test_target_default(self) -> None:
        assert job(source=".").selection.target == os.getcwd()

    def test_target(self) -> None:
        assert job(target="test").selection.target == os.path.abspath("test")

    def test_source_as_target(self) -> None:
        assert job(source_as_target=True).selection.target == os.getcwd()

    ##
    # [rename]
    ##

    def test_backup_folder(self) -> None:
        assert job(backup_folder="/tmp").rename.backup_folder == "/tmp"

    def test_best_format(self) -> None:
        assert job(best_format=True).rename.best_format is True

    def test_dry_run(self) -> None:
        assert job(dry_run=True).rename.dry_run is True

    def test_move_action(self) -> None:
        assert job(move_action="copy").rename.move_action == "copy"

    def test_cleaning_action(self) -> None:
        assert job(cleaning_action="backup").rename.cleaning_action == "backup"

    ##
    # [filters]
    ##

    def test_album_complete(self) -> None:
        assert job(album_complete=True).filters.album_min is None
        assert job(album_complete=True).filters.album_complete is True

    def test_album_min(self) -> None:
        assert job(album_min=19).filters.album_min == 19
        assert job(album_min=19).filters.album_complete is False

    def test_extension(self) -> None:
        assert job(extension="lol").filters.extension == ["lol"]

    def test_field_skip(self) -> None:
        assert job(field_skip="album").filters.field_skip == "album"

    ##
    # [template_settings]
    ##

    def test_shell_friendly(self) -> None:
        assert job(shell_friendly=True).template_settings.shell_friendly is True

    ##
    # [cli_output]
    ##

    def test_color(self) -> None:
        assert job(color=True).cli_output.color is True

    def test_debug(self) -> None:
        assert job(debug=True).cli_output.debug is True

    def test_job_info(self) -> None:
        assert job(job_info=True).cli_output.job_info is True

    def test_mb_track_listing(self) -> None:
        assert job(mb_track_listing=True).cli_output.mb_track_listing is True

    def test_one_line(self) -> None:
        assert job(one_line=True).cli_output.one_line is True

    def test_stats(self) -> None:
        assert job(stats=True).cli_output.stats is True

    def test_verbose(self) -> None:
        assert job(verbose=True).cli_output.verbose is True

    ##
    # [metadata_actions]
    ##

    def test_enrich_metadata(self) -> None:
        assert job(enrich_metadata=True).metadata_actions.enrich_metadata is True

    def test_remap_classical(self) -> None:
        assert job(remap_classical=True).metadata_actions.remap_classical is True


def get_config_path(config_file: str) -> str:
    return helper.get_testfile("config", config_file)


def make_job_with_config(config_file: str) -> Job:
    args = ArgsDefault()
    args.config = [get_config_path(config_file)]
    return Job(args)


class TestJobWithConfigParser:
    def setup_method(self) -> None:
        self.job = make_job_with_config("all-true.ini")

    def test_minimal_config_file(self) -> None:
        job = make_job_with_config("minimal.ini")
        assert job.rename.backup_folder == "/tmp/minimal"

    def test_multiple_config_files(self) -> None:
        args = ArgsDefault()
        args.config = [
            get_config_path("all-true.ini"),
            get_config_path("minimal.ini"),
        ]
        job = Job(args)
        assert job.rename.backup_folder == "/tmp/minimal"
        assert job.filters.genre_classical == ["sonata", "opera"]

    def test_multiple_config_file_different_order(self) -> None:
        args = ArgsDefault()
        args.config = [
            get_config_path("minimal.ini"),
            get_config_path("all-true.ini"),
        ]
        job = Job(args)
        assert job.rename.backup_folder == "/tmp/backup"

    def test_section_selection(self) -> None:
        assert self.job.selection.source == "/tmp"
        assert self.job.selection.target == "/tmp"
        assert self.job.selection.source_as_target is True

    def test_section_rename(self) -> None:
        assert self.job.rename.backup_folder == "/tmp/backup"
        assert self.job.rename.best_format is True
        assert self.job.rename.dry_run is True
        assert self.job.rename.move_action == "copy"
        assert self.job.rename.cleaning_action == "delete"

    def test_section_filters(self) -> None:
        assert self.job.filters.album_complete is True
        assert self.job.filters.album_min == 42
        assert self.job.filters.extension == ["wave", "aiff"]
        assert self.job.filters.genre_classical == ["sonata", "opera"]
        assert self.job.filters.field_skip == "comment"

    def test_section_template_settings(self) -> None:
        assert self.job.template_settings.classical is True
        assert self.job.template_settings.shell_friendly is True
        assert self.job.template_settings.no_soundtrack is True

    def test_section_path_templates(self) -> None:
        assert self.job.path_templates.default == "classical"
        assert self.job.path_templates.compilation == "classical"
        assert self.job.path_templates.soundtrack == "classical"
        assert self.job.path_templates.classical == "classical"

    def test_section_cli_output(self) -> None:
        assert self.job.cli_output.color is True
        assert self.job.cli_output.debug is True
        assert self.job.cli_output.job_info is True
        assert self.job.cli_output.mb_track_listing is True
        assert self.job.cli_output.one_line is True
        assert self.job.cli_output.stats is True
        assert self.job.cli_output.verbose is True

    def test_section_metadata_actions(self) -> None:
        assert self.job.metadata_actions.enrich_metadata is True
        assert self.job.metadata_actions.remap_classical is True


class TestTimer:
    def setup_method(self) -> None:
        self.timer = Timer()

    def get_result(self, begin: float, end: float) -> str:
        self.timer.begin = begin
        self.timer.end = end
        return self.timer.result()

    def test_method_start(self) -> None:
        self.timer.start()
        assert self.timer.begin > 0

    def test_method_stop(self) -> None:
        self.timer.stop()
        assert self.timer.end > 0

    def test_method_result(self) -> None:
        assert self.get_result(10.3475, 14.594) == "4.2s"

    def test_method_result_large(self) -> None:
        assert self.get_result(10, 145) == "135.0s"

    def test_method_result_small(self) -> None:
        assert self.get_result(10.00001, 10.00002) == "0.0s"


class TestCounter:
    def setup_method(self) -> None:
        self.counter = Counter()

    def test_reset(self) -> None:
        self.counter.count("lol")
        self.counter.reset()
        assert self.counter.get("lol") == 0

    def test_count(self) -> None:
        self.counter.count("rename")
        assert self.counter.get("rename") == 1
        self.counter.count("rename")
        assert self.counter.get("rename") == 2

    def test_result(self) -> None:
        self.counter.count("rename")
        assert self.counter.result() == "rename=1"

        self.counter.count("no_field")
        assert self.counter.result() == "no_field=1 rename=1"
