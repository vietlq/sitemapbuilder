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
	find src -name __pycache__ -exec rm -rf {} \;
	find src -name *.pyc -exec rm -rf {} \;
	find tests -name __pycache__ -exec rm -rf {} \;
	find tests -name *.pyc -exec rm -rf {} \;

venv:
	@echo "deactivate"
	@echo "rm -rf _venv"
	@echo "virtualenv -p python3 _venv"
	@echo "source _venv/bin/activate"
	@echo "pip install -r requirements.txt"
