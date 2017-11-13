project := backend
test_folder := tests

export PYTHONPATH=.

.PHONY: bootstrap
bootstrap: clean
	sh scripts/bootstrap.sh

.PHONY: clean
clean:
	sh scripts/clean.sh

.PHONY: clean_port
clean_port:
	fuser -k 8888/tcp

.PHONY: reset_db
reset_db:
	sh scripts/clean.sh
	sh scripts/reset_db.sh

.PHONE: makemigrations
makemigrations:
	python ./backend_core/manage.py makemigrations

.PHONE: migrate
migrate:
	python ./backend_core/manage.py migrate

.PHONE: test_data
test_data:
	python ./backend_core/manage.py loaddata test_data.json

.PHONY: server
server:
	export DJANGO_SETTINGS_MODULE="backend_core.settings.dev"
	python ./backend_core/manage.py runserver 0.0.0.0:8888
