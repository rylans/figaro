test:
	python figaro.py
	python -m doctest README.md
	nosetests -v

install:
	pip install .
