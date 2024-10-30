from django.urls import path, include
from monitoring.views import site_and_calibration_view, FuelLevelView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('sites-calibrations/', site_and_calibration_view, name='site_and_calibration'),  # URL pour les sites et calibrations
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/fuel-level/', FuelLevelView.as_view(), name='fuel-level'),
]