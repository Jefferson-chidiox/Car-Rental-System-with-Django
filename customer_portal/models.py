from django.db import models
from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from car_dealer_portal.models import *
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)


class Testimonial(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  name = models.TextField()
  email = models.TextField()
  text = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Testimonial by {self.user.username if self.user else 'Anonymous'}"


class Query(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  name = models.TextField()
  email = models.TextField()
  text = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Query by {self.user.username if self.user else 'Anonymous'}"
