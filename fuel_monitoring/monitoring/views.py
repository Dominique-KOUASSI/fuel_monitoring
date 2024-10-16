from django.shortcuts import render
from .models import Site_info, Calibration_info

def site_and_calibration_view(request):
    sites = Site_info.objects.all()  # Récupère tous les sites
    calibrations = Calibration_info.objects.all()  # Récupère toutes les calibrations
    return render(request, 'monitoring/site_and_calibration.html', {'sites': sites, 'calibrations': calibrations})