from django.shortcuts import render
from monitoring.models import Site_info, Calibration_info, FuelLevel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from monitoring.permissions import IsIotUserAuthenticated

from monitoring.serializers import FuelLevelSerializer

from django.utils import timezone

def site_and_calibration_view(request):
    sites = Site_info.objects.all()  # Récupère tous les sites
    calibrations = Calibration_info.objects.all()  # Récupère toutes les calibrations
    return render(request, 'monitoring/site_and_calibration.html', {'sites': sites, 'calibrations': calibrations})



class FuelLevelView(APIView):
    permission_classes = [IsIotUserAuthenticated]  # Autorise uniquement les utilisateurs authentifiés

    def post(self, request):
        # Instancier le serializer avec les données envoyées dans la requête
        serializer = FuelLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Sauvegarder les données dans la base de données
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def fuel_level_trends(request):
    sites = Site_info.objects.all()  # La liste des sites disponibles
    selected_site = None  # Site sélectionné
    fuel_levels = []  # Par défaut, aucune donnée

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_site = request.POST.get('site_name')  # Récupérer le site sélectionné

        # Vérifier que toutes les données nécessaires sont disponibles
        if start_date and end_date and selected_site:
            # Convertir les dates en objets datetime si nécessaire
            start_date = timezone.make_aware(timezone.datetime.fromisoformat(start_date))
            end_date = timezone.make_aware(timezone.datetime.fromisoformat(end_date))
            
            # Récupérer les niveaux de carburant filtrés
            fuel_levels = FuelLevel.objects.filter(
                timestamp__range=[start_date, end_date],
                site__site_name=selected_site
            ).order_by('timestamp')

    # Renvoyer le contexte complet, peu importe la méthode (GET ou POST)
    return render(request, 'monitoring/fuel_level_trends.html', {
        'sites': sites,
        'fuel_levels': fuel_levels,
        'selected_site': selected_site,  # Passer le site sélectionné
        'start_date': request.POST.get('start_date', ''),
        'end_date': request.POST.get('end_date', ''),
    })