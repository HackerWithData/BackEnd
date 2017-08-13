project := backend
test_folder := tests

export PYTHONPATH=.

.PHONY: bootstrap
bootstrap: clean
	sh scripts/bootstrap.sh

.PHONY: clean
clean:
	sh scripts/clean.sh
