test:
	poetry run tox

install: update

clear_poetry_cache:
	poetry cache clear PyPI --all --no-interaction
	poetry cache clear _default_cache --all --no-interaction

# https://github.com/python-poetry/poetry/issues/34#issuecomment-1054626460
install_editable:
	pip install -e .

update: clear_poetry_cache
	poetry lock
	poetry install

build:
	poetry build

publish:
	poetry build
	poetry publish

format:
	poetry run tox -e format

docs:
	poetry run tox -e docs
	xdg-open docs/_build/index.html > /dev/null 2>&1

lint:
	poetry run tox -e lint

pin_docs_requirements:
	pip-compile --output-file=docs/requirements.txt docs/requirements.in pyproject.toml

.PHONY: test install install_editable update build publish format docs lint pin_docs_requirements
