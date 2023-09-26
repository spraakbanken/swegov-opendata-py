

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = poetry run
else
  INVENV =
endif

PROJECT := swegov_opendata

.PHONY: help
help:
	@echo "usage:"
	@echo "install-dev (alias: dev)"
	@echo "		installs the project for development"

	@echo "install"
	@echo "		installs the project for deployment"

	@echo "install-ci"
	@echo "		installs the project for CI"

	@echo "test"
	@echo "		run given test(s) (default: tests='tests')"

	@echo "test-w-coverage"
	@echo "		run given test(s) with coverage information (default: all_tests='tests')"

dev: install-dev
install-dev:
	poetry install

install:
	poetry install --only main --sync

# setup CI environment
install-ci: install-dev
	poetry install --only ci

default_cov := "--cov=${PROJECT}"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

.PHONY: test
test:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=${cov_report} ${all_tests}

watch-test:
	${INVENV} watchfiles "pytest -vvv tests" swegov_opendata tests
