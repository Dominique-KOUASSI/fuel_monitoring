from django.shortcuts import render
from monitoring.models import Site_info, Calibration_info, FuelLevel

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from monitoring.permissions import IsIotUserAuthenticated

from monitoring.serializers import FuelLevelSerializer

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