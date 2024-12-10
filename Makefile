config := $(HOME)/.config/snip.json
data_dir := $(HOME)/Sync/snip-data

build:
	hatchling build

qa: lint
	pytest -v

run: lint
	python3 sn.py put foo
	python3 sn.py get foo

lint: format
	ruff check . --fix

format:
	ruff check --select I --fix .
	ruff format .

rmconfig:
	-rm $(config)

catconfig:
	jq . $(config)

ls:
	ls -l $(data_dir)

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -fr build
