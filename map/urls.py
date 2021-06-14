from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bikestation', views.bikestation, name='bikestation'),
]