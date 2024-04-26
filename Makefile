
test: clean-cache
	pip install -q -e '.[testing]' \
	&& tox -e test

lint:
	# flake8 --config .flake8 compose_pydantic
	tox -e static-analysis

clean: clean-cache

clean-cache: clean-cache
	rm -rf tmp.pypi* dist/* build/* \
	&& rm -rf src/*.egg-info/
	find . -name '*.tmp.*' -delete
	find . -name '*.pyc' -delete
	find . -name  __pycache__ -delete
	find . -type d -name .tox | xargs -n1 -I% bash -x -c "rm -rf %"

build: lint test
	python3 -m build

check:
	twine check dist/*

upload:
	twine upload --skip-existing dist/*
