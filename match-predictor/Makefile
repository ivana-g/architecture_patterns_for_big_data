SHELL = /usr/bin/env bash -o pipefail

default: help

.PHONY: help
help:
	# Usage:
	@sed -n '/^\([a-z][^:]*\).*/s//    make \1/p' $(MAKEFILE_LIST)

.PHONY: backend/install
backend/install:
	cd backend && \
	python3 -m venv env && \
	env/bin/pip install --upgrade pip setuptools wheel && \
	env/bin/pip install -r requirements.txt

.PHONY: backend/types
backend/types:
	cd backend && \
	env/bin/mypy matchpredictor test fakecsvprovider

.PHONY: backend/test
backend/test: backend/types
	cd backend && \
	env/bin/python -m unittest

.PHONY: backend/measure
backend/measure:
	cd backend && \
	env/bin/python -m unittest discover -p "measure_*.py"

.PHONY: backend/report
backend/report:
	cd backend && \
	env/bin/python report.py

.PHONY: backend/run
backend/run:
	cd backend && \
	. .env && \
	env/bin/python -m matchpredictor

.PHONY: frontend/lint
frontend/lint:
	npm --prefix frontend run lint

.PHONY: frontend/test
frontend/test: frontend/lint
	npm --prefix frontend test

.PHONY: frontend/install
frontend/install:
	npm --prefix frontend install

.PHONY: frontend/run
frontend/run:
	npm --prefix frontend start

.PHONY: integration/install
integration/install:
	npm --prefix integration-tests install

.PHONY: integration/test
integration/test:
	cd integration-tests && \
	. ../backend/env/bin/activate && \
	./run

.PHONY: integration/run
integration/run:
	cd integration-tests && \
	. ../backend/env/bin/activate && \
	KEEP_OPEN=true ./run

.PHONY: install
install: backend/install frontend/install integration/install

.PHONY: unittest
unittest: backend/test frontend/test

.PHONY: test
test: unittest integration/test
