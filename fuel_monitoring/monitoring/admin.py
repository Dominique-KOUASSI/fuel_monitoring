from django.contrib import admin

# Register your models here.

from monitoring.models import Site_info, Calibration_info, FuelLevel

# Définir l'administration pour le modèle Site_info
class Site_info_dmin(admin.ModelAdmin):
    list_display = ('date_created', 'site_name', 'city', 'longitude', 'latitude')  # Champs à afficher dans la liste

# Définir l'administration pour le modèle Listing
class Calibration_info_admin(admin.ModelAdmin):
    list_display = ('date_created', 'fuel_level', 'fuel_volume', 'site')  # Ajouter 'band' pour voir le groupe associé

# Définir l'administration pour le modèle FuelLevel
class Fuel_level_admin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'site')
    #list_display = ('timestamp', 'level')

# Enregistrer les modèles dans l'admin
admin.site.register(Site_info, Site_info_dmin)
admin.site.register(Calibration_info, Calibration_info_admin)
admin.site.register(FuelLevel, Fuel_level_admin)