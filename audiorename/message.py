"""Print messages on the command line."""

from .args import all_fields
from collections import OrderedDict
import ansicolor
import audiorename
import phrydy
import tmep
import typing
if typing.TYPE_CHECKING:
    from .job import Job
    from .audiofile import AudioFile
    from .meta import Meta


class KeyValue:

    kv: "OrderedDict[str, str]"

    def __init__(self, color: bool = False):
        self.color = color
        self.kv = OrderedDict()

    def add(self, key: str, value: str) -> None:
        self.kv[key] = value

    def result(self) -> str:
        out = ''
        for key, value in self.kv.items():
            key = key + ':'
            if self.color:
                key = ansicolor.yellow(key)
            out = out + key + ' ' + value + '\n'
        return out

    def result_one_line(self) -> str:
        out: typing.List[str] = []
        for key, value in self.kv.items():
            if self.color:
                key = ansicolor.green(key)
            out.append(key + '=' + str(value))

        return ' '.join(out)


class Message:
    """Print messages on the command line interface.

    :param job: The `job` object.
    :type job: audiorename.job.Job
    """

    color: bool
    verbose: bool
    one_line: bool

    def __init__(self, job: "Job"):
        self.color = job.cli_output.color
        self.verbose = job.cli_output.verbose
        self.one_line = job.cli_output.one_line
        self.max_field = self.max_fields_length()
        self.indent_width = 4

    @staticmethod
    def max_fields_length() -> int:
        return phrydy.doc_generator.get_max_field_length(all_fields)

    def output(self, text: str = '') -> None:
        if self.one_line:
            print(text.strip(), end=' ')
        else:
            print(text)

    def template_indent(self, level: int = 1) -> str:
        return (' ' * self.indent_width) * level

    def template_path(self, audio_file: 'AudioFile') -> str:
        path: str
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.short

        if self.color:
            if audio_file.type == 'source':
                path = ansicolor.magenta(path)
            else:
                path = ansicolor.yellow(path)

        return path

    def next_file(self, audio_file: 'AudioFile'):
        print()
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.dir_and_file
        if self.color:
            path = ansicolor.blue(path, reverse=True)
        self.output(path)

    def action_one_path(self, message: str, audio_file: 'AudioFile') -> None:
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(audio_file))
        self.output()

    def action_two_path(self, message: str, source: 'AudioFile',
                        target: 'AudioFile') -> None:
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(source))
        self.output(self.template_indent(2) + 'to:')
        self.output(self.template_indent(2) + self.template_path(target))

    def best_format(self, best: typing.Literal['target', 'source'], attr: str,
                    source: 'Meta', target: 'Meta') -> None:
        source_attr = getattr(source, attr)
        target_attr = getattr(target, attr)

        if source_attr == target_attr and best == 'target':
            self.output('Best format: Source and target have the same formats,'
                        ' use target.')
        else:
            self.output(
                'Best format is “' + best + '” because of “' + attr + '”: '
                '(source: ' + str(source_attr) + ', '
                'target: ' + str(target_attr) + ')'
            )

    def diff(self, key: str, value1: str, value2: str):
        key_width = self.max_field + 2
        value2_indent = self.indent_width + key_width
        key += ':'
        key = key.ljust(self.max_field + 2)

        def quote(value: typing.Any):
            return '“' + str(value) + '”'

        value1 = quote(value1)
        value2 = quote(value2)
        if self.color:
            value1 = ansicolor.red(value1)
            value2 = ansicolor.green(value2)
            key = ansicolor.yellow(key)
        self.output(self.template_indent(1) + key + value1)
        self.output(' ' * value2_indent + value2)

    def status_color(self, status: typing.Literal['ok', 'error', 'progress']
                     ) -> typing.Literal['yellow', 'red', 'green']:
        if status == 'progress':
            return 'yellow'
        elif status == 'error':
            return 'red'
        else:
            return 'green'

    def status(self, text: str,
               status: typing.Literal['ok', 'error', 'progress']):
        if self.color:
            color = getattr(ansicolor, self.status_color(status))
            text = color(text, reverse=True)
        self.output(self.template_indent(1) + text)


def job_info(job: 'Job') -> None:
    versions = KeyValue(job.cli_output.color)
    versions.add('audiorename', audiorename.__version__)
    versions.add('phrydy', phrydy.__version__)
    versions.add('tmep', tmep.__version__)

    info = KeyValue(job.cli_output.color)
    info.add('Versions', versions.result_one_line())
    info.add('Action', job.rename.move_action)
    info.add('Source', job.selection.source)
    info.add('Target', job.selection.target)
    if job.rename.cleaning_action == 'backup':
        info.add('Backup folder', job.rename.backup_folder)

    if job.cli_output.verbose:
        info.add('Default', job.path_templates.default)
        info.add('Compilation', job.path_templates.compilation)
        info.add('Soundtrack', job.path_templates.soundtrack)

    print(info.result())


def stats(job: 'Job') -> None:
    kv = KeyValue(job.cli_output.color)

    kv.add('Execution time', job.stats.timer.result())
    kv.add('Counter', job.stats.counter.result())
    print(kv.result())
