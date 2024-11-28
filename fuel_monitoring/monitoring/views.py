from django.contrib.auth.decorators import login_required

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
    

@login_required
def fuel_level_trends_bakup(request):
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



@login_required  # Assure que seuls les utilisateurs connectés accèdent à cette vue
def fuel_level_trends(request):
    user = request.user  # Utilisateur connecté
    sites = Site_info.objects.filter(user=user)  # Filtrer les sites liés à l'utilisateur
    selected_site = None
    fuel_levels = []

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_site = request.POST.get('site_name')  # Récupérer le site sélectionné

        if start_date and end_date and selected_site:
            # Convertir les dates au format timezone-aware
            start_date_dt = timezone.make_aware(timezone.datetime.fromisoformat(start_date))
            end_date_dt = timezone.make_aware(timezone.datetime.fromisoformat(end_date))

            # Filtrer les niveaux de carburant pour le site sélectionné et la plage de dates
            fuel_levels = FuelLevel.objects.filter(
                site__site_name=selected_site,
                site__user=user,  # Assurez-vous que le site appartient à l'utilisateur connecté
                timestamp__range=(start_date_dt, end_date_dt)
            ).order_by('timestamp')

    return render(request, 'monitoring/fuel_level_trends.html', {
        'sites': sites,
        'fuel_levels': fuel_levels,
        'selected_site': selected_site,
        'start_date': request.POST.get('start_date', ''),
        'end_date': request.POST.get('end_date', ''),
    })