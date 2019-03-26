"""Print messages on the command line."""

from audiorename.args import all_fields
from collections import OrderedDict
import ansicolor
import audiorename
import phrydy
import tmep


class KeyValue(object):

    def __init__(self, color=False):
        self.color = color
        self.kv = OrderedDict()

    def add(self, key, value):
        self.kv[key] = value

    def result(self):
        out = ''
        for key, value in self.kv.items():
            key = key + ':'
            if self.color:
                key = ansicolor.yellow(key)
            out = out + key + ' ' + value + '\n'
        return out

    def result_one_line(self):
        out = []
        for key, value in self.kv.items():
            if self.color:
                key = ansicolor.green(key)
            out.append(key + '=' + str(value))

        return ' '.join(out)


class Message(object):
    """Print messages on the command line interface.

    :param job: The `job` object.
    :type job: audiorename.job.Job
    """

    def __init__(self, job):
        self.color = job.output.color
        self.verbose = job.output.verbose
        self.one_line = job.output.one_line
        self.max_field = self.max_fields_length()
        self.indent_width = 4

    @staticmethod
    def max_fields_length():
        return phrydy.doc.get_max_field_length(all_fields)

    def output(self, text=''):
        if self.one_line:
            print(text.strip(), end=' ')
        else:
            print(text)

    def template_indent(self, level=1):
        return (' ' * self.indent_width) * level

    def template_path(self, audio_file):
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

    def next_file(self, audio_file):
        print()
        if self.verbose:
            path = audio_file.abspath
        else:
            path = audio_file.dir_and_file
        if self.color:
            path = ansicolor.blue(path, reverse=True)
        self.output(path)

    def action_one_path(self, message, audio_file):
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(audio_file))
        self.output()

    def action_two_path(self, message, source, target):
        self.status(message, status='progress')
        self.output(self.template_indent(2) + self.template_path(source))
        self.output(self.template_indent(2) + 'to:')
        self.output(self.template_indent(2) + self.template_path(target))

    def best_format(self, best, attr, source, target):
        source_attr = getattr(source, attr)
        target_attr = getattr(target, attr)

        if source_attr == target_attr and best == 'target':
            self.output('Best format: Source and target have the some formats,'
                        ' use target.')
        else:
            self.output(
                'Best format is “' + best + '” because of “' + attr + '”: '
                '(source: ' + str(source_attr) + ', '
                'target: ' + str(target_attr) + ')'
            )

    def diff(self, key, value1, value2):
        key_width = self.max_field + 2
        value2_indent = self.indent_width + key_width
        key += ':'
        key = key.ljust(self.max_field + 2)

        def quote(value):
            return '“' + str(value) + '”'

        value1 = quote(value1)
        value2 = quote(value2)
        if self.color:
            value1 = ansicolor.red(value1)
            value2 = ansicolor.green(value2)
            key = ansicolor.yellow(key)
        self.output(self.template_indent(1) + key + value1)
        self.output(' ' * value2_indent + value2)

    def status_color(self, status):
        if status == 'progress':
            return 'yellow'
        elif status == 'error':
            return 'red'
        else:
            return 'green'

    def status(self, text, status):
        if self.color:
            color = getattr(ansicolor, self.status_color(status))
            text = color(text, reverse=True)
        self.output(self.template_indent(1) + text)


def job_info(job):
    """
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """
    versions = KeyValue(job.output.color)
    versions.add('audiorename', audiorename.__version__)
    versions.add('phrydy', phrydy.__version__)
    versions.add('tmep', tmep.__version__)

    info = KeyValue(job.output.color)
    info.add('Versions', versions.result_one_line())
    info.add('Action', job.rename.move)
    info.add('Source', job.source)
    info.add('Target', job.target)
    if job.rename.cleanup == 'backup':
        info.add('Backup folder', job.rename.backup_folder)

    if job.output.verbose:
        info.add('Default', job.format.default)
        info.add('Compilation', job.format.compilation)
        info.add('Soundtrack', job.format.soundtrack)

    print(info.result())


def stats(job):
    """
    :param job: The `job` object.
    :type job: audiorename.job.Job
    """
    kv = KeyValue(job.output.color)

    kv.add('Execution time', job.stats.timer.result())
    kv.add('Counter', job.stats.counter.result())
    print(kv.result())
