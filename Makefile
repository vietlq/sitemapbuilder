.PHONY: help lint style clean venv

help:
	@echo "help             Show this help"
	@echo "lint             Run linter (pylint)"
	@echo "style            Run style check (flake8)"

lint:
	pylint src tests

style:
	flake8 src tests

clean:
	rm -rf .pytest_cache/ .cache/

venv:
	@echo "deactivate"
	@echo "rm -rf _venv"
	@echo "virtualenv -p python3 _venv"
	@echo "pip install -r requirements.txt"
