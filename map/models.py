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

class BusRoutes(models.Model):
    route_id = models.CharField(max_length = 45)
    agency_id = models.CharField(max_length = 45)
    route_short_name = models.CharField(max_length = 45)
    route_long_name = models.CharField(max_length = 45)
    route_type = models.IntegerField()

class BusShapes(models.Model):
    shape_id = models.CharField(max_length = 45)
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.FloatField()

class BusStopTimes(models.Model):
    trip_id = models.CharField(max_length = 45)
    arrival_time = models.CharField(max_length = 45)
    departure_time = models.CharField(max_length = 45)
    stop_id = models.CharField(max_length = 45)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length = 45)
    pickup_type = models.IntegerField()
    drop_off_type = models.IntegerField()
    shape_dist_traveled = models.FloatField()

class BusStops(models.Model):
    stop_id = models.CharField(max_length = 45)
    stop_name = models.CharField(max_length = 45)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()

class BusTransfers(models.Model):
    from_stop_id = models.CharField(max_length = 45)
    to_stop_id = models.CharField(max_length = 45)
    transfer_type = models.IntegerField()
    min_transfer_time = models.IntegerField()

class BusTrips(models.Model):
    route_id = models.CharField(max_length = 45)
    service_id = models.CharField(max_length = 45)
    trip_id = models.CharField(max_length = 45)
    shape_id = models.CharField(max_length = 45)
    trip_headsign = models.CharField(max_length = 45)
    direction_id = models.IntegerField()

class RouteData(models.Model):
    ShapeID = models.CharField(max_length = 45)
    StopSequence = models.IntegerField()
    RouteName = models.CharField(max_length = 45)
    RouteDescription = models.CharField(max_length = 45)
    Direction = models.CharField(max_length = 45)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    ShortCommonName_en = models.CharField(max_length = 45)
    HasPole = models.CharField(max_length = 45)
    HasShelter = models.CharField(max_length = 45)
    RouteData = models.CharField(max_length = 45)
