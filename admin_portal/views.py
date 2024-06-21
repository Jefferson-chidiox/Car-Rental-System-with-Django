# admin_portal/views.py
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from car_dealer_portal.models import CarDealer, Vehicles, Area
from customer_portal.models import *
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import AdminRegistrationForm, AdminLoginForm, AdminPasswordChangeForm

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True  # Ensure the user is set as superuser (admin)
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Correct password handling
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_portal/admin_register.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_portal/admin_login.html', {'form': form, 'error': 'Invalid credentials or not an admin'})
    else:
        form = AdminLoginForm()
    return render(request, 'admin_portal/admin_login.html', {'form': form})

@login_required
def admin_password_change(request):
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('admin_dashboard')
    else:
        form = AdminPasswordChangeForm(user=request.user)
    return render(request, 'admin_portal/admin_password_change.html', {'form': form})


def logout_view(request):
  # Log out the user and redirect to login page
  auth.logout(request)
  return render(request, 'home/home.html')


@login_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_bookings = Orders.objects.count()
    total_queries = Query.objects.count() if Query.objects.exists() else 0
    total_testimonials = Testimonial.objects.count() if Testimonial.objects.exists() else 0
    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_queries': total_queries,
        'total_testimonials': total_testimonials,
    }
    return render(request, 'admin_portal/dashboard.html', context)

@login_required
def view_users(request):
    car_dealers = CarDealer.objects.select_related('car_dealer').all()
    customers = Customer.objects.select_related('user').all()

    context = {
        'car_dealers': car_dealers,
        'customers': customers,
    }
    return render(request, 'admin_portal/view_users.html', context)

@login_required
def view_bookings(request):
    bookings = Orders.objects.select_related('user', 'vehicle', 'car_dealer').all()

    context = {
        'bookings': bookings,
    }
    return render(request, 'admin_portal/view_bookings.html', context)

@login_required
def view_testimonials(request):
    testimonials = Testimonial.objects.select_related('user').all()

    context = {
        'testimonials': testimonials,
    }
    return render(request, 'admin_portal/view_testimonials.html', context)

@login_required
def view_queries(request):
    queries = Query.objects.all() if Query.objects.exists() else []

    context = {
        'queries': queries,
    }
    return render(request, 'admin_portal/view_queries.html', context)

