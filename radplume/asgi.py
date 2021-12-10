import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from decouple import config
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()

bokeh_config = apps.get_app_config('bokeh_server_django')

application = ProtocolTypeRouter({
    'http':  get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(bokeh_config.routes.get_websocket_urlpatterns())),
})
