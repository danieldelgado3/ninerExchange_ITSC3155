from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    #image = models.ImageField(upload_to='media')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1_url = models.URLField() 
    image2_url = models.URLField(blank=True, null=True)
    image3_url = models.URLField(blank=True, null=True)
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='listings', null=True, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser): #gives everything django user model has, plus a name field
    name = models.CharField(max_length=200, null=True)

class CampusLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
