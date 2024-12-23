web: gunicorn app:app --workers 4 --timeout 60
worker: celery -A app.celery worker --loglevel=info