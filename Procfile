web: gunicorn HNKMSMEOTCAPP.wsgi --bind 0.0.0.0:$PORT --timeout 120 --log-level debug --workers 2 --preload --log-file
web:python manage.py migrate && gunicorn HNKMSMEOTCAPP.wsgi