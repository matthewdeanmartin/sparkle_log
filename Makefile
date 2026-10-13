.EXPORT_ALL_VARIABLES:
# Get changed files

FILES := $(wildcard **/*.py)

# if you wrap everything in uv run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := uv run
else
    VENV :=
endif

uv.lock: pyproject.toml
	@echo "Installing dependencies"
	@uv sync --all-extras

clean-pyc:
	@echo "Removing compiled files"


clean-test:
	@echo "Removing coverage data"
	@rm -f .coverage || true
	@rm -f .coverage.* || true

clean: clean-pyc clean-test

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
test: clean uv.lock install_plugins
	@echo "Running unit tests"
	# $(VENV) pytest --doctest-modules sparkle_log
	# $(VENV) python -m unittest discover
	$(VENV) pytest tests -vv -n 2 --cov=sparkle_log --cov-report=html --cov-fail-under 48 --cov-branch --cov-report=xml --junitxml=junit.xml -o junit_family=legacy --timeout=5 --session-timeout=600
	$(VENV) bash ./scripts/basic_checks.sh
#	$(VENV) bash basic_test_with_logging.sh



isort:
	@echo "Formatting imports"
	$(VENV) isort .

.PHONY: isort

.PHONY: jiggle_version

jiggle_version:
ifeq ($(CI),true)
	@echo "Running in CI mode"
	$(VENV) jiggle_version check
else
	@echo "Running locally"
	$(VENV) jiggle_version hash-all
	# jiggle_version bump --increment auto
endif

black: isort jiggle_version
	@echo "Formatting code"
	$(VENV) metametameta pep621
	$(VENV) black sparkle_log # --exclude .venv
	$(VENV) black tests # --exclude .venv
	$(VENV) git2md sparkle_log --ignore __init__.py __pycache__ --output SOURCE.md

.PHONY: black

pre-commit: isort black
	@echo "Pre-commit checks"
	$(VENV) pre-commit run --all-files

.PHONY: pre-commit

bandit:
	@echo "Security checks"
	$(VENV)  bandit sparkle_log -r --quiet

.PHONY: bandit

.PHONY: pylint
pylint: isort black
	@echo "Linting with pylint"
	$(VENV) ruff check --fix
	$(VENV) pylint sparkle_log --fail-under 9.8

# for when using -j (jobs, run in parallel)
.NOTPARALLEL: isort black

check: mypy test pylint bandit

# ── Python 3.15 trial run ─────────────────────────────────────────────────────
# Uses a dedicated venv so the normal .venv is never touched.

PY315 := 3.15.0rc2
VENV315 := .venv315rc2
PY315_EXE := $(VENV315)/Scripts/python.exe

.PHONY: venv315
venv315:
	@echo "Creating Python $(PY315) trial venv at $(VENV315)"
	@test -x $(PY315_EXE) || uv venv $(VENV315) --python $(PY315)
	uv pip install -e . pytest pytest-cov pytest-timeout pytest-mock pytest-asyncio pytest-randomly --python $(PY315_EXE)

.PHONY: venv315-clean
venv315-clean:
	@echo "Recreating Python $(PY315) trial venv from scratch"
	uv venv $(VENV315) --python $(PY315) --clear
	@$(MAKE) venv315

.PHONY: test315
test315: venv315
	@echo "Running unit tests on Python $(PY315)"
	$(PY315_EXE) -m pytest tests -q --timeout=60 -p no:randomly -p no:sugar

.PHONY: check315
check315: test315
	@echo "Python $(PY315) checks passed."


.PHONY: publish
publish: test
	rm -rf dist && $(VENV) hatch build

.PHONY: mypy
mypy:
	$(VENV) echo $$PYTHONPATH
	$(VENV) mypy sparkle_log --ignore-missing-imports --check-untyped-defs


check_docs:
	$(VENV) interrogate sparkle_log --verbose  --fail-under 70
	$(VENV) pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse"

make_docs:
	pdoc sparkle_log --html -o docs --force

check_md:
	$(VENV) linkcheckMarkdown README.md
	$(VENV) markdownlint README.md --config .markdownlintrc
	$(VENV) mdformat README.md docs/*.md


check_spelling:
	$(VENV) pylint sparkle_log --enable C0402 --rcfile=.pylintrc_spell
	$(VENV) pylint docs --enable C0402 --rcfile=.pylintrc_spell
	$(VENV) codespell README.md --ignore-words=private_dictionary.txt
	$(VENV) codespell sparkle_log --ignore-words=private_dictionary.txt
	$(VENV) codespell docs --ignore-words=private_dictionary.txt

check_changelog:
	# pipx install keepachangelog-manager
	$(VENV) kaclm validate

check_all_docs: check_docs check_md check_spelling check_changelog

check_self:
	# Can it verify itself?
	$(VENV) ./scripts/dog_food.sh

#audit:
#	# $(VENV) python -m sparkle_log audit
#	$(VENV) tool_audit single sparkle_log --version=">=2.0.0"

install_plugins:
	echo "N/A"

.PHONY: issues
issues:
	echo "N/A"

# ── Dogfooding targets (independent, not wired into check) ───────────────────

.PHONY: version-check
version-check:
	@uv run jiggle_version check

.PHONY: dev-status
dev-status:
	@uv run troml-dev-status validate .

.PHONY: prerelease-check
prerelease-check: version-check dev-status
	@echo "Pre-release checks passed."

.PHONY: dont-be-lazy
dont-be-lazy:
	@uv run dont_be_lazy --root . --no-color summary
	@uv run dont_be_lazy --root . --no-color scan sparkle_log --no-config-suppressions || true

.PHONY: pydoc-docs
pydoc-docs:
	@uv run pydoc_fork sparkle_log -o ./pydoc/
