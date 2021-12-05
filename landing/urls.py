from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('equations/', views.equations, name='equations'),
    path('about/', views.about, name='about'),
]
