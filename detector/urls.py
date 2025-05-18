from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect, name='detect'),
    path('prevention/', views.prevention, name='prevention'),
    path('resources/', views.resources, name='resources'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('health/', views.health_check, name='health_check'),
] 