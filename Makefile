.PHONY: venv activate install lint format run-weatherapp

venv:
	pip install uv
	uv venv

activate:
	source .venv/bin/activate

install:
	uv pip install -e .
	uv pip install -r requirements.txt

lint:
	uv run ruff check

format:
	uv run ruff format

run-weatherapp:
	streamlit run weatherapp/app.py
