project := backend
test_folder := tests

export PYTHONPATH=.

.PHONY: bootstrap
bootstrap: clean
	sh scripts/bootstrap.sh

.PHONY: bootstrap_db
bootstrap_db: drop_db create_db

.PHONY: create_db
create_db:
	python database_python_scripts/database.py create
	echo "Create database"

.PHONY: drop_db
drop_db:
	python database_python_scripts/database.py drop
	echo "Drop database"

.PHONY: upgrade_db
upgrade_db:
	alembic upgrade head
	echo "upgrade database"

.PHONY: downgrade_db
downgrade_db:
	alembic downgrade -1
	echo "downgrade database" 

.PHONY: clean
clean:
	sh scripts/clean.sh

.PHONY: server
server:
	python ./backend_core/manage.py runserver 0.0.0.0:6060
