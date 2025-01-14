.PHONY: all build clean format lint run test version

all: lint format build test run

build:
	uv build

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build dist .venv .ruff_cache .pytest_cache

format:
	uv run ruff check --select I --fix .  # Sort imports
	uv run ruff format .                  # Format

lint:
	uv run ruff check . --fix

run: 
	uv run snip ls

test: lint format
	uv run pytest -v

version:
	uv run snip --version
