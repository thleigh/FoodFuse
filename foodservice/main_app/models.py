from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Restaurant(models.Model):
    location = models.CharField(max_length=100)
    restaurant = models.CharField(max_length=100)
    delivery_fee = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name
