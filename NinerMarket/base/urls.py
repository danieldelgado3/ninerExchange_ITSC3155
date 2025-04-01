from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"), #Homepage URL
    path('login/', views.login, name='login'), #Login page URL
]