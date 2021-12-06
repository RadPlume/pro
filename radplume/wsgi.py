import os

from django.core.wsgi import get_wsgi_application
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{config("PROJECT_NAME")}.settings')

application = get_wsgi_application()
