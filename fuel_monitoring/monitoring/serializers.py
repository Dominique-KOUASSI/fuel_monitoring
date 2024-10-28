from rest_framework import serializers

from monitoring.models import FuelLevel

class FuelLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLevel
        fields = ['level', 'timestamp', 'site']  # Inclure les champs que vous souhaitez exposer dans l'API
