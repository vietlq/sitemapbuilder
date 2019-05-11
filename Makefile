.PHONY: help lint style venv

help:
	@echo "help             Show this help"
	@echo "lint             Run linter (pylint"
	@echo "style            Run style check (flake8)"

lint:
	pylint tests

style:
	flake8 tests