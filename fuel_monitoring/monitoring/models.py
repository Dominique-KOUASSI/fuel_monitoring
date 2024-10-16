from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Site_info(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    site_name = models.CharField(max_length=255)
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
    site = models.ForeignKey(Site_info, null=True, on_delete=models.CASCADE)  # clé étrangère vers Site_info

    def __str__(self):
        return self.fuel_type