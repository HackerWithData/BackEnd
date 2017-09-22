echo "Reset database"
find ./backend_core -path "*/db.sqlite3" -delete
find ./backend_core -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ./backend_core -path "*/migrations/*.pyc"  -delete
python ./backend_core/manage.py makemigrations
python ./backend_core/manage.py migrate