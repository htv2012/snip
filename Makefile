config := $(HOME)/.config/snip.json
data_dir := $(HOME)/Sync/snip-data

run: lint
	uv run snip ls

build: lint
	uv build

qa: lint
	pytest -v

lint: format
	uv run ruff check . --fix

format:
	uv run ruff check --select I --fix .
	uv run ruff format .

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build dist .venv .ruff_cache
