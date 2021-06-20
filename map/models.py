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

class MapAllroutedata(models.Model):
    shapeid = models.IntegerField(db_column='ShapeID', blank=True, null=True)  # Field name made lowercase.
    stopsequence = models.CharField(db_column='StopSequence', max_length=45, blank=True, null=True)  # Field name made lowercase.
    atcocode = models.CharField(db_column='AtcoCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    routename = models.CharField(db_column='RouteName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    routedesc = models.CharField(db_column='RouteDesc', max_length=45, blank=True, null=True)  # Field name made lowercase.
    direction = models.CharField(db_column='Direction', max_length=45, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=45, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=45, blank=True, null=True)  # Field name made lowercase.
    shortcommonname_en = models.CharField(db_column='ShortCommonName_en', max_length=45, blank=True, null=True)  # Field name made lowercase.
    haspole = models.CharField(db_column='HasPole', max_length=45, blank=True, null=True)  # Field name made lowercase.
    hasshelter = models.CharField(db_column='HasShelter', max_length=45, blank=True, null=True)  # Field name made lowercase.
    routedata = models.CharField(db_column='RouteData', max_length=45, blank=True, null=True)  # Field name made lowercase.
    route = models.CharField(db_column='Route', max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAP_allroutedata'