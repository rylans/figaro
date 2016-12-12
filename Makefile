test:
	python -m figaro.agent
	python -m figaro.handlers
	python -m figaro.response
	python -m figaro.memorykeys
	python -m doctest README.md
	nosetests -v

install:
	pip install .
