from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, FileExtensionValidator, MaxValueValidator
from django.contrib.auth.models import User

# Define the Area model
class Area(models.Model):
    pincode = models.CharField(validators=[MinLengthValidator(6), MaxLengthValidator(6)], max_length=6, unique=True)  # Pincode with length constraints
    city = models.CharField(max_length=20)  # City name

    def __str__(self):
        return f"{self.city} ({self.pincode})"  # String representation of Area

# Define the CarDealer model
class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relation with Django's User model
    mobile = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(13)], max_length=13)  # Mobile number with length constraints
    area = models.OneToOneField(Area, on_delete=models.PROTECT)  # One-to-one relation with Area, protecting the area from deletion
    wallet = models.IntegerField(default=0)  # Wallet balance

    def __str__(self):
        return self.car_dealer.username  # String representation of CarDealer

# Define the Vehicles model
class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key for the vehicle
    car_name = models.CharField(max_length=20)  # Car name
    car_model = models.CharField(max_length=20, default="Unknown")  # Car model with a default value
    dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)  # Foreign key to CarDealer, protecting the dealer from deletion
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)  # Foreign key to Area, setting to null if area is deleted
    capacity = models.IntegerField()  # Seating capacity of the vehicle
    is_available = models.BooleanField(default=True)  # Availability status of the vehicle
    description = models.CharField(max_length=100)  # Description of the vehicle
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True,  # Image upload field
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),  # Allowed file types
            MaxValueValidator(5 * 1024 * 1024)  # Max file size (5MB)
        ])

    def __str__(self):
        return self.car_name  # String representation of Vehicle

