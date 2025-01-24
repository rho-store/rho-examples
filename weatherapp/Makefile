.PHONY: venv activate install lint format run

venv:
	pip install uv
	uv venv

activate:
	source .venv/bin/activate

install:
	uv pip install -r requirements.txt

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

run:
	streamlit run app.py
