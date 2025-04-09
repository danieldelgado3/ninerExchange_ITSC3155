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