# AGENTS.md

## Commands
- `make test` - Run tests
- `make check` - Run all checks (mypy, test, pylint, bandit, pre-commit)
- `make black` - Format code
- `make publish` - Build and publish

## Rules
- Run `make black` before commit
- Run `make test` before publish
- Minimum test coverage: 48%
- Pylint score: 9.8+
- Docstring coverage: 70%+
