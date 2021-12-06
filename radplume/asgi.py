import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from decouple import config
from django.apps import apps

bokeh_config = apps.get_app_config('bokeh_server_django')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()

application = ProtocolTypeRouter({
    'http':  AuthMiddlewareStack(URLRouter(bokeh_config.routes.get_http_urlpatterns())),
    'websocket': AuthMiddlewareStack(URLRouter(bokeh_config.routes.get_websocket_urlpatterns())),
})