from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"), #Homepage URL
    path('login/', views.login_view, name='login'), #Login page URL
    path('settings/', views.settings, name='settings'), #Settings page 
    path('addItems/', views.addItems, name='addItems'), #addItem page URL
    path('addItemsToCloudinary/', views.addItemsToCloudinary, name='addItemsToCloudinary'), #addItem page URL
]