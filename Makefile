test:
	python -m figaro.agent
	python -m figaro.response
	python -m figaro.memorykeys
	python -m figaro.handlerbase
	python -m figaro.handlers.arithmetichandler
	python -m figaro.handlers.convoterminationhandler
	python -m figaro.handlers.declarationhandler
	python -m figaro.handlers.declaredmemoryhandler
	python -m figaro.handlers.elizastatementhandler
	python -m figaro.handlers.greetingstatementhandler
	python -m doctest README.md
	nosetests -v

install:
	pip install .
