all: run

build: lint
	uv build

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build dist .venv .ruff_cache

format:
	uv run ruff check --select I --fix .
	uv run ruff format .

lint: format
	uv run ruff check . --fix

qa: lint
	pytest -v

run: lint
	uv run snip ls

test:
	uv run pytest -v

version:
	uv run snip --version
