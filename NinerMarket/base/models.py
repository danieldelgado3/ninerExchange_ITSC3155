from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media')
    image1_url = models.URLField() 
    image2_url = models.URLField(blank=True, null=True)
    image3_url = models.URLField(blank=True, null=True)