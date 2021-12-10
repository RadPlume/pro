from bokeh.server.django import autoload, static_extensions
from django.apps import apps
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import plume.pn_app as plume_app

pn_app_onfig = apps.get_app_config('bokeh_server_django')

urlpatterns = [
    path('', include('landing.urls')),
    path('plume/', include('plume.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()

bokeh_apps = [
    autoload("plume", plume_app.app),
]
