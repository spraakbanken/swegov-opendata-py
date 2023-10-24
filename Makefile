

.default: help

ifeq (${VIRTUAL_ENV},)
  INVENV = rye run
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

	@echo "fmt"
	@echo "		format all python files"

	@echo "check-fmt"
	@echo "		check formatting for all python files"

	@echo "lint"
	@echo "		lint all code"

	@echo "type-check"
	@echo "		type-check all code"

dev: install-dev
install-dev:
	rye sync

install:
	rye sync --no-dev

# setup CI environment
install-ci: install-dev
	rye sync --features=ci

default_cov := "--cov=src/${PROJECT}"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

.PHONY: test
test:
	${INVENV} pytest -vv ${tests}

.PHONY: watch-test
watch-test:
	${INVENV} watchfiles "pytest -vvv tests" src tests

.PHONY: test-w-coverage
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=${cov_report} ${all_tests}

.PHONY: watch-test-w-coverage
watch-test-w-coverage:
	${INVENV} watchfiles "pytest -vv ${cov} --cov-report=${cov_report} ${all_tests}" src tests pyproject.toml

fmt:
	${INVENV} black src tests

.PHONY: check-fmt
check-fmt:
	${INVENV} black --check src tests

.PHONY: lint
lint:
	rye run lint:ruff

# type-check the code
.PHONY: type-check
type-check:
	${INVENV} mypy --config-file mypy.ini src tests
