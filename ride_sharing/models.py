from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ride(models.Model):
  rider = models.ForeignKey(User, related_name = "ride_requests", on_delete=models.CASCADE)
  origin = models.CharField(max_length=100)
  destination = models.CharField(max_length=100)
  asset_capacity = models.IntegerField()
  travel_date = models.DateField()
  travel_medium = models.CharField(max_length=100, choices = [("Car", "Car"), ("Bus", "Bus"), ("Train", "Train")])

  def __str__(self):
    return f"{self.rider.username} - {self.origin} - {self.destination} - {self.asset_capacity} - {self.travel_date}"

class AssetTransportationRequest(models.Model):
  requester = models.ForeignKey(User, related_name = "transport_requests", on_delete=models.CASCADE)
  origin = models.CharField(max_length=100)
  destination = models.CharField(max_length=100)
  asset_type = models.CharField(max_length=100, 
                                choices=[("LAPTOP", "Vehicle"), ("TRAVEL_BAG", "Travel Bag"), ("PACKAGE", "Package")])
  number_of_assets = models.IntegerField()
  sensitivity = models.CharField(max_length=100, choices=[("HIGHLY_SENSITIVE", "Highly Sensitive"), ("SENSITIVE", "Sensitive"), ("NORMAL", "Normal")])
  status = models.CharField(max_length=100, choices=[("PENDING", "Pending"), ("EXPIRED", "Expired")], 
    default="PENDING")
  request_date = models.DateField()

  def __str__(self):
    return f"{self.requester.username} - {self.origin} - {self.destination} - {self.asset_type} - {self.number_of_assets} - {self.sensitivity} - {self.status} - {self.request_date}"

class MatchedRides(models.Model):
  ride = models.ForeignKey(Ride, on_delete = models.CASCADE)
  asset_transportation_request = models.ForeignKey(AssetTransportationRequest, on_delete = models.CASCADE)
  status = models.CharField(max_length = 100, default = "NOT_APPLIED", choices = [("NOT_APPLIED", "Not Applied"), ("APPLIED", "Applied")])