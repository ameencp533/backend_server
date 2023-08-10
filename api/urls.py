# api/urls.py
from django.urls import path
from .views import configure_device_view

urlpatterns = [
    path('configure-device/', configure_device_view, name='configure-device'),
]
