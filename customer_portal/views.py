from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth

from customer_portal.forms import QueryForm, TestimonialForm
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from car_dealer_portal.models import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def index(request):
  # If user is not authenticated, redirect to login page
  if not request.user.is_authenticated:
    return render(request, 'customer/login.html')
  else:
    user = User.objects.get(username=request.user)
    orders = Orders.objects.filter(user=user, is_complete=False)
    vehicles = Vehicles.objects.filter(is_available=True)  # Get ALL vehicles

    # --- Pagination for vehicles ---
    paginator = Paginator(vehicles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # ---

    # Pass both orders and vehicles to homepage.html
    return render(request, 'customer/home_page.html', {
      'orders': orders,
      'vehicles': page_obj,  # Pass the paginated vehicles
    })

def login(request):
  # Render the login page
  return render(request, 'customer/login.html')

def auth_view(request):
  # Authenticate and log in the user
  if request.user.is_authenticated:
    return render(request, 'customer/home_page.html')
  else:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    try:
      customer = Customer.objects.get(user=user)
    except:
      customer = None
    if customer is not None:
      auth.login(request, user)
      return render(request, 'customer/home_page.html')
    else:
      return render(request, 'customer/login_failed.html')

def logout_view(request):
  # Log out the user and redirect to login page
  auth.logout(request)
  return render(request, 'customer/login.html')

def register(request):
  # Render the registration page
  return render(request, 'customer/register.html')

def registration(request):
  # Register the user and create a new customer profile
  username = request.POST['username']
  password = request.POST['password']
  mobile = request.POST['mobile']
  firstname = request.POST['firstname']
  lastname = request.POST['lastname']
  email = request.POST['email']
  city = request.POST['city']
  city = city.lower()
  pincode = request.POST['pincode']

  try:
    user = User.objects.create_user(username=username, password=password, email=email)
    user.first_name = firstname
    user.last_name = lastname
    user.save()
  except:
    return render(request, 'customer/registration_error.html')
  try:
    area = Area.objects.get(city=city, pincode=pincode)
  except:
    area = None
  if area is not None:
    customer = Customer(user=user, mobile=mobile, area=area)
  else:
    area = Area(city=city, pincode=pincode)
    area.save()
    area = Area.objects.get(city=city, pincode=pincode)
    customer = Customer(user=user, mobile=mobile, area=area)

  customer.save()
  return render(request, 'customer/registered.html')

def search(request):
  # Render the search page
  return render(request, 'customer/search.html')

def search_results(request):
  # Handle search results based on user input
  city = request.POST.get('city', '').lower()
  vehicle_name = request.POST.get('vehicle_name', '')
  car_model = request.POST.get('car_model', '')
  capacity = request.POST.get('capacity', '')
  vehicles_list = []
  areas = Area.objects.filter(city=city) if city else Area.objects.all()

  for area in areas:
    vehicles = Vehicles.objects.filter(area=area, is_available=True)

    # Apply filters
    if vehicle_name:
      vehicles = vehicles.filter(car_name__icontains=vehicle_name)
    if car_model:
      vehicles = vehicles.filter(car_model__icontains=car_model)
    if capacity:
      vehicles = vehicles.filter(capacity=capacity)

    for car in vehicles:
      vehicle_dictionary = {
        'name': car.car_name,
        'car_model': car.car_model,
        'image_url': car.image.url if car.image else None,
        'id': car.id,
        'pincode': car.area.pincode,
        'capacity': car.capacity,
        'description': car.description
      }
      vehicles_list.append(vehicle_dictionary)
  request.session['vehicles_list'] = vehicles_list
  return render(request, 'customer/search_results.html')

@login_required
def rent_vehicle(request):
  # Render the vehicle rent confirmation page
  id = request.POST['id']
  vehicle = Vehicles.objects.get(id=id)
  cost_per_day = int(vehicle.capacity) * 13
  return render(request, 'customer/confirmation.html', {'vehicle': vehicle, 'cost_per_day': cost_per_day})

@login_required
def confirm(request):
  # Confirm the vehicle rent and create an order
  vehicle_id = request.POST['id']
  username = request.user
  user = User.objects.get(username=username)
  days = request.POST['days']
  vehicle = Vehicles.objects.get(id=vehicle_id)
  if vehicle.is_available:
    car_dealer = vehicle.dealer
    rent = (int(vehicle.capacity)) * 13 * (int(days))
    car_dealer.wallet += rent
    car_dealer.save()
    try:
      order = Orders(vehicle=vehicle, car_dealer=car_dealer, user=user, rent=rent, days=days)
      order.save()
    except:
      order = Orders.objects.get(vehicle=vehicle, car_dealer=car_dealer, user=user, rent=rent, days=days)
    vehicle.is_available = False
    vehicle.save()
    return render(request, 'customer/confirmed.html', {'order': order})
  else:
    return render(request, 'customer/order_failed.html')

@login_required
def manage(request):
  # Manage the user's active orders
  order_list = []
  user = User.objects.get(username=request.user)
  try:
    orders = Orders.objects.filter(user=user)
  except:
    orders = None
  if orders is not None:
    for o in orders:
      if o.is_complete == False:
        order_dictionary = {'id': o.id, 'rent': o.rent, 'vehicle': o.vehicle, 'days': o.days,
                            'car_dealer': o.car_dealer}
        order_list.append(order_dictionary)
  return render(request, 'customer/manage.html', {'od': order_list})

@login_required
def update_order(request):
  # Update an existing order and make the vehicle available again
  order_id = request.POST['id']
  order = Orders.objects.get(id=order_id)
  vehicle = order.vehicle
  vehicle.is_available = True
  vehicle.save()
  car_dealer = order.car_dealer
  car_dealer.wallet -= int(order.rent)
  car_dealer.save()
  order.delete()
  cost_per_day = int(vehicle.capacity) * 13
  return render(request, 'customer/confirmation.html', {'vehicle': vehicle}, {'cost_per_day': cost_per_day})

@login_required
def delete_order(request):
  # Delete an existing order and update the car dealer's wallet
  order_id = request.POST['id']
  order = Orders.objects.get(id=order_id)
  car_dealer = order.car_dealer
  car_dealer.wallet -= int(order.rent)
  car_dealer.save()
  vehicle = order.vehicle
  vehicle.is_available = True
  vehicle.save()
  order.delete()
  return HttpResponseRedirect('/customer_portal/manage/')

def submit_query(request):
    if request.method == 'POST':
      form = QueryForm(request.POST)
      if form.is_valid():
        query = form.save(commit=False)
        if request.user.is_authenticated:
          query.user = request.user
        query.save()
        return redirect('home_page.html')
    else:
      form = QueryForm()
    return render(request, 'customer/submit_query.html', {'form': form})


def submit_testimonial(request):
  if request.method == 'POST':
    form = TestimonialForm(request.POST)
    if form.is_valid():
      testimonial = form.save(commit=False)
      if request.user.is_authenticated:
        testimonial.user = request.user
      testimonial.save()
      return redirect('home_page.html')
  else:
    form = TestimonialForm()
  return render(request, 'customer/submit_testimonial.html', {'form': form})
