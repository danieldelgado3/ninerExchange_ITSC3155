from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Listing, Universities

# Register your models here.

from .models import Listing
admin.site.register(CustomUser, UserAdmin)

admin.site.register(Listing)
admin.site.register(Universities) 
