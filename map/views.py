from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import *
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def bikestation(request):
	ret = BikeStation.objects.all()
	data = serializers.serialize("json", ret, ensure_ascii=False)
	return HttpResponse(data)