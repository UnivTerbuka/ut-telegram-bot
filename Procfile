web: gunicorn app:app --max-requests 1200 --timeout 300 --workers=1
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade