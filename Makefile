.PHONY: install
install:
	python3.9 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

.PHONY: dbsetup
dbsetup:
	source venv/bin/activate && python -m youtube.db

.PHONY: run
run:
	source venv/bin/activate && uvicorn yt.main:app --reload

.PHONY: lint
lint:
	flake8 youtube tests

.PHONY: typing
typing:
	mypy youtube tests

.PHONY: test
test:
	pytest

.PHONY: coverage
coverage:
	pytest --cov=youtube --cov-report term-missing

.PHONY: ci
ci: lint typing test
