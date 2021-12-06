from django.urls import path
from . import views

app_name = 'radplume'
urlpatterns = [
    path('', views.plume, name='radplume'),
]
