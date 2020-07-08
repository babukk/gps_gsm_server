
make_migr:
		. ./.venv3/bin/activate; \
		python manage.py makemigrations gpsserver; \
		python manage.py migrate; \
		deactivate

show_migr:
		. ./.venv3/bin/activate; \
		python manage.py makemigrations --dry-run --verbosity 3; \
		deactivate
