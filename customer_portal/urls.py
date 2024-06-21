from django.urls import path,include, re_path

from customer_portal import views
from customer_portal.views import *
from home import views as home_views


urlpatterns = [
    re_path(r'^index/$',index),
    re_path(r'^login/$',login),
    re_path(r'^auth/$',auth_view),
    re_path(r'^logout/$',logout_view),
    re_path(r'^register/$',register),
    re_path(r'^registration/$',registration),
    re_path(r'^search/$',search),
    re_path(r'^search_results/$',search_results),
    re_path(r'^rent/$',rent_vehicle),
    re_path(r'^confirmed/',confirm),
    re_path(r'^manage/',manage),
    re_path(r'^update/',update_order),
    re_path(r'^delete/',delete_order),
    re_path(r'^submit_query/',submit_query),
    re_path(r'^submit_testimonial/',submit_testimonial),
]
