from django.urls import path
from .views import site_and_calibration_view

urlpatterns = [
    path('sites-calibrations/', site_and_calibration_view, name='site_and_calibration'),  # URL pour les sites et calibrations
]