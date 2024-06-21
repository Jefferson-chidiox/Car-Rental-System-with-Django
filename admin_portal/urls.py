from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.view_users, name='view_users'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('queries/', views.view_queries, name='view_queries'),
    path('testimonials/', views.view_testimonials, name='view_testimonials'),
    path('login/', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),
    path('password_change/', views.admin_password_change, name='admin_password_change'),
    path('logout/', views.logout_view),

]
