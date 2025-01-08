.PHONY: all build clean format lint run test version

all: format lint test run

build: lint test
	uv build

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build dist .venv .ruff_cache

format:
	uv run ruff check --select I --fix .
	uv run ruff format .

lint:
	uv run ruff check . --fix

run: 
	uv run snip ls

test:
	uv run pytest -v

version:
	uv run snip --version
