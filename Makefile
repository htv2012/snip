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

version:
	@echo "Version reported by snip:"
	@uv run snip --version

	@echo ""
	@echo "Version reported by hatchling:"
	@uv run hatchling version

	@echo ""
	@echo To set the version, run 
	@echo "    uv run hatchling version <new>"
	@echo "For example:"
	@echo "    uv run hatchling version 0.5.14"

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build dist .venv .ruff_cache
