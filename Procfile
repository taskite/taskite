release: python3 manage.py migrate
web: gunicorn taskite.wsgi
worker: celery -A taskite worker -l INFO