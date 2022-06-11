"""Read the configuration file in the INI format."""

import configparser

from .args import ArgsDefault


def read_config_file(file_path) -> ArgsDefault:
    config = configparser.ConfigParser()
    config.read(file_path)

    options = {}

    args = ArgsDefault()

    for section in config.sections():
        for option in config.options(section):
            options[option] = config.get(section, option)

    for attr in dir(args):
        if '__' not in attr and attr in options:
            setattr(args, attr, options[attr])

    return args
