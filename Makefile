.PHONY: venv
venv:
	python3.9 -m venv venv

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: lint
lint:
	flake8 TechSwap tests

.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	pytest --cov=TechSwap --cov=swapshop --cov-report term-missing

.PHONY: ci
ci: lint coverage
