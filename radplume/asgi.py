import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': get_asgi_application(),
})
