#MAPI
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapi, name='mapi'),
]

