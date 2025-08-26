# Environment
PYTHON := python

# Code quality
.PHONY: code.format code.lint code.check
code.format:
	ruff format

code.lint: code.format
	ruff check --exit-non-zero-on-fix
	slotscheck src
	mypy

code.check: code.lint