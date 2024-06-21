from django.core.checks import messages
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.shortcuts import render
from django.db.models import ProtectedError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from car_dealer_portal.models import *
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.

# View for the index page, checks if the user is authenticated and renders the appropriate page
def index(request):
  if not request.user.is_authenticated:
    return render(request, 'car_dealer/login.html')
  else:
    return render(request, 'car_dealer/home_page.html')


# View for rendering the login page
def login(request):
  return render(request, 'car_dealer/login.html')


# Authentication view to log in the user, checks credentials and redirects to home or login_failed
def auth_view(request):
  if request.user.is_authenticated:
    return render(request, 'car_dealer/home_page.html')
  else:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    try:
      car_dealer = CarDealer.objects.get(car_dealer=user)
    except:
      car_dealer = None
    if car_dealer is not None:
      auth.login(request, user)
      return render(request, 'car_dealer/home_page.html')
    else:
      return render(request, 'car_dealer/login_failed.html')


# View to log out the user and render the login page
def logout_view(request):
  auth.logout(request)
  return render(request, 'car_dealer/login.html')


# View to render the registration page
def register(request):
  return render(request, 'car_dealer/register.html')


# Registration view to create a new user and car dealer, handles user and area creation
def registration(request):
  username = request.POST['username']
  password = request.POST['password']
  mobile = request.POST['mobile']
  firstname = request.POST['firstname']
  lastname = request.POST['lastname']
  email = request.POST['email']
  city = request.POST['city'].lower()
  pincode = request.POST['pincode']

  try:
    user = User.objects.create_user(username=username, password=password, email=email)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
  except:
    return render(request, 'car_dealer/registration_error.html')

  try:
    area = Area.objects.get(city=city, pincode=pincode)
  except:
    area = None

  if area is not None:
    car_dealer = CarDealer(car_dealer=user, mobile=mobile, area=area)
  else:
    area = Area(city=city, pincode=pincode)
    area.save()
    area = Area.objects.get(city=city, pincode=pincode)
    car_dealer = CarDealer(car_dealer=user, mobile=mobile, area=area)
  car_dealer.save()
  return render(request, 'car_dealer/registered.html')


# View to add a new vehicle, handles vehicle creation and image upload
@login_required
def add_vehicle(request):
  car_name = request.POST['car_name']
  car_model = request.POST['car_model']
  cd = CarDealer.objects.get(car_dealer=request.user)
  city = request.POST['city'].lower()
  pincode = request.POST['pincode']
  description = request.POST['description']
  capacity = request.POST['capacity']

  try:
    area = Area.objects.get(city=city, pincode=pincode)
  except Area.DoesNotExist:
    area = Area(city=city, pincode=pincode)
    area.save()
    area = Area.objects.get(city=city, pincode=pincode)

  if request.FILES.get('image'):
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    image_url = fs.url(filename)
  else:
    image_url = None

  car = Vehicles(
    car_name=car_name,
    car_model=car_model,
    dealer=cd,
    area=area,
    description=description,
    capacity=capacity,
    image=image_url
  )
  car.save()
  return render(request, 'car_dealer/vehicle_added.html')


# View to manage vehicles, lists all vehicles for the logged-in dealer
@login_required
def manage_vehicles(request):
  username = request.user
  user = User.objects.get(username=username)
  car_dealer = CarDealer.objects.get(car_dealer=user)
  vehicle_list = Vehicles.objects.filter(dealer=car_dealer)
  return render(request, 'car_dealer/manage.html', {'vehicle_list': vehicle_list})


# View to list orders for the logged-in dealer, filters only incomplete orders
@login_required
def order_list(request):
  username = request.user
  user = User.objects.get(username=username)
  car_dealer = CarDealer.objects.get(car_dealer=user)
  orders = Orders.objects.filter(car_dealer=car_dealer, is_complete=False)
  return render(request, 'car_dealer/order_list.html', {'order_list': orders})


# View to mark an order as complete, updates the vehicle availability and redirects to order list
@login_required
def complete(request):
  order_id = request.POST['id']
  order = Orders.objects.get(id=order_id)
  vehicle = order.vehicle
  order.is_complete = True
  order.save()
  vehicle.is_available = True
  vehicle.save()
  return HttpResponseRedirect('/car_dealer_portal/order_list/')


# View to display the history of orders and earnings for the logged-in dealer
@login_required
def history(request):
  user = User.objects.get(username=request.user)
  car_dealer = CarDealer.objects.get(car_dealer=user)
  orders = Orders.objects.filter(car_dealer=car_dealer)
  return render(request, 'car_dealer/history.html', {'wallet': car_dealer.wallet, 'order_list': orders})


# View to delete a vehicle, handles exceptions if the vehicle is associated with active orders
@login_required
def delete(request):
  veh_id = request.POST['id']
  try:
    vehicle = Vehicles.objects.get(id=veh_id)
    vehicle.delete()
    return HttpResponseRedirect('/car_dealer_portal/manage_vehicles/')
  except ProtectedError:
    vehicle_list = Vehicles.objects.filter(dealer__car_dealer=request.user)
    error_message = "Cannot delete this vehicle because it's associated with active orders."
    return render(request, 'car_dealer/manage.html', {'vehicle_list': vehicle_list, 'error_message': error_message})


