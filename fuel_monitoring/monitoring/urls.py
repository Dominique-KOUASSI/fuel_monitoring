from django.urls import path
from monitoring.views import site_and_calibration_view, FuelLevelView

urlpatterns = [
    path('sites-calibrations/', site_and_calibration_view, name='site_and_calibration'),  # URL pour les sites et calibrations
    path('api/fuel-level/', FuelLevelView.as_view(), name='fuel-level'),
]