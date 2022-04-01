test: cleancache
	pytest ./tests

lint:
	flake8 --config .flake8 compose_pydantic

cleancache:
	rm -Rf .pytest_cache
	cd compose_pydantic ; python3 -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	cd compose_pydantic ; python3 -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"
	cd tests ; python3 -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	cd tests ; python3 -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"

build: lint test
	python3 -m build

check:
	twine check dist/*

upload:
	twine upload --skip-existing dist/*