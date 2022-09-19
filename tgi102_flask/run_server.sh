

gunicorn --bind=0.0.0.0:8003 --log-level info --workers 4 app:app
