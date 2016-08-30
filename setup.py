from setuptools import setup

setup(
	name = 'audiorename',
	version = '0.0.1',
	author = 'Josef Friedrich',
	author_email = 'josef@friedrich.rocks',
	description = ('Rename audio files from metadata tags.'),
	license = 'MIT',
	packages = ['audiorename'],
	keywords = 'audio',
	url = 'https://github.com/Josef-Friedrich/audiorename',
	install_requires = [
		'phrydy', 'tmep', 'ansicolor',
	],
	scripts = ['bin/audiorenamer'],
	classifiers = [
		'Development Status :: 3 - Alpha',
	],
	zip_safe=False,
)
