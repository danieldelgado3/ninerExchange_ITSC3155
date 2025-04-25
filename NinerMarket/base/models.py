from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Listing(models.Model):
    name = models.CharField(max_length=255, unique = True)
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
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    university = models.ForeignKey('Universities', on_delete=models.SET_NULL, null=True, blank=True)

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/profile.png'
    
class Universities(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CampusLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

