from django.urls import path 
from . import views

urlpatterns = [
    path('', views.geo, name='geo'),
]