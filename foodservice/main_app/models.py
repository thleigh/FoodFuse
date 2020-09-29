from django.db import models
from django.contrib.auth.models import User

# Create your models here.
## RESTAURANT - FULL CRUD ROUTE
## CREATE, READ, UPDATE, DELETE

class Restaurant(models.Model):
    location = models.CharField(max_length=100)
    restaurant = models.CharField(max_length=100)
    delivery_fee = models.CharField(max_length=100)
    delivery_time = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    restaurants = models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='/default.jpg', upload_to='media')
    # if has image:
    #     return 'default.jpg'
    # else:
    #     return 'default.jpg'

    def __str__(self):
        return f'{self.user.username} Profile'