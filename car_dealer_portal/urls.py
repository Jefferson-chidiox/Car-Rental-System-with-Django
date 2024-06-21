from django.urls import path,include, re_path
from car_dealer_portal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^index/$',index),
    re_path(r'^login/$',login),
    re_path(r'^auth/$',auth_view),
    re_path(r'^logout/$',logout_view),
    re_path(r'^register/$',register),
    re_path(r'^registration/$',registration),
    re_path(r'^add_vehicle/$',add_vehicle),
    re_path(r'^manage_vehicles/$',manage_vehicles),
    re_path(r'^order_list/$',order_list),
    re_path(r'^complete/$',complete),
    re_path(r'^history/$',history),
    re_path(r'^delete/$',delete),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
