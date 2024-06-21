from django.shortcuts import render
from car_dealer_portal.models import *

def home_page(request):
    # Fetch the first 6 available vehicles from the database
    vehicles = Vehicles.objects.filter(is_available=True)[:6]
    # Render the 'home.html' template with the vehicles data
    return render(request, 'home/home.html', {'vehicles': vehicles})

def index(request):
    # Render the 'index.html' template
    return render(request, 'home/index.html')
