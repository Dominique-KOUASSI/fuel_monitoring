from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Site_info(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    site_name = models.CharField(max_length=255)
    #site_name = models.CharField(max_length=100, unique=True)  # Ajoutez unique=True ici
    site_name = models.CharField(max_length=100, primary_key=True)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.site_name
    
class Calibration_info(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    fuel_type = models.CharField(max_length=50, default='DIESEL')
    fuel_level = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(4095)])
    fuel_volume = models.IntegerField()
    #site = models.ForeignKey(Site_info, on_delete=models.CASCADE)
    #site = models.ForeignKey(Site_info, null=True, on_delete=models.CASCADE)  # clé étrangère vers Site_info
    site = models.ForeignKey(Site_info, to_field='site_name', on_delete=models.CASCADE)
    #site = models.ForeignKey(Site_info, to_field='site_name', on_delete=models.CASCADE, default='AC795_IRATEKE')  # clé étrangère vers Site_info
    #site = models.ForeignKey(Site_info, on_delete=models.CASCADE)

    def __str__(self):
        return self.fuel_type

#class FuelLevel(models.Model):
#    level = models.FloatField()                             # Champ pour le niveau de carburant
#    timestamp = models.DateTimeField(auto_now_add=True)     # Enregistrement automatique de la date et heure
#    site = models.ForeignKey(Site_info, null=True, on_delete=models.CASCADE)  # clé étrangère vers Site_info

#    def __str__(self):
#        return f"Fuel level: {self.level, self.site}"

class FuelLevel(models.Model):
    level = models.FloatField()  # Champ pour le niveau de carburant
    timestamp = models.DateTimeField(auto_now_add=True)  # Enregistrement de l'heure
    #site = models.ForeignKey(Site_info, on_delete=models.CASCADE)
    site = models.ForeignKey(Site_info, to_field='site_name', on_delete=models.CASCADE)
    #site = models.ForeignKey(Site_info, to_field='site_name', null=True, on_delete=models.CASCADE)  # clé étrangère vers Site_info
    #site = models.ForeignKey(Site_info, to_field='site_name', on_delete=models.CASCADE, default='AC795_IRATEKE')   # clé étrangère vers Site_info
    #site = models.ForeignKey(Site_info, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fuel level: {self.level}, Site: {self.site}"


class fuel_level_average(models.Model):
    average = models.FloatField()  # Champ pour le niveau de carburant
    calculated_at = models.DateTimeField(auto_now_add=True)  # Enregistrement de l'heure