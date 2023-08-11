# api/urls.py
from django.urls import path
from .views import configure_device_view, data_collector_view

urlpatterns = [
    path('configure-device/', configure_device_view, name='configure-device'),
    path('data-collector/', data_collector_view, name='configure-device'),
]
