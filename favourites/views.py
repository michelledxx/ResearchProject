from django.shortcuts import render, redirect, HttpResponse
from users.models import my_stations
# Create your views here.
from favourites import get_schedule
import json


def stations(request):
	return render(request, 'mystations.html')

def check_auth(request):
    if request.user.is_authenticated:
        current_user = request.user
        station_id = '8220DB000354'
        user_fav = my_stations(stop_id = station_id, user = current_user)
        user_fav.save()
        show_favs(request)
        return render(request, 'mystations.html')
    else:
        return render(request, 'mystations.html')


def show_favs(request):
    if request.user.is_authenticated:
        current_user = request.user
        vals = my_stations.objects.values('stop_id').filter(user=current_user)
        s = get_schedule.get_times('8220DB000354')
        return HttpResponse(s)

