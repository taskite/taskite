release: python3 manage.py migrate
web: gunicorn calyvim.wsgi
worker: celery -A calyvim worker -l INFO