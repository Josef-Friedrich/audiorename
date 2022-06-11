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

    for k, v in vars(args).items():
        if k in options:
            setattr(args, k, v)

    return args
