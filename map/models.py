from django.db import models

# Create your models here.
class BikeStation(models.Model):
    bk_id = models.IntegerField(primary_key=True, null = False)
    bk_contract_name = models.CharField(max_length = 45)
    bk_name = models.CharField(max_length = 45)
    bk_address = models.CharField(max_length = 45)
    bk_lat = models.FloatField()
    bk_lng = models.FloatField()
    bk_banking = models.CharField(max_length = 45)
    bk_bouns = models.CharField(max_length = 45)
    bk_bike_stands = models.IntegerField()
    bk_available_bike_stands = models.IntegerField()
    bk_available_bikes = models.IntegerField()
    bk_status = models.CharField(max_length = 45)
    bk_last_update = models.CharField(max_length = 45)