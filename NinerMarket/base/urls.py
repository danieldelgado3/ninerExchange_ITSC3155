from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"), #Homepage URL
    path('login/', views.login_view, name='login'), #Login page URL
    path('logout/', views.logout_view, name='logout'), #Logout URL
    path('settings/', views.settings, name='settings'), #Settings page 
    path('addItems/', views.addItems, name='addItems'), #addItem page URL
    path('addItemsToCloudinary/', views.addItemsToCloudinary, name='addItemsToCloudinary'), #addItem page URL
    path('signup/', views.signup_view, name = 'signup'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('campus-map/', views.campusPickup, name='campus_map'), #Campus Map
    path('listing/<int:listing_id>/delete/', views.delete_listing, name='delete_listing'),
    path('profile/', views.profile, name='profile'),
    path('campus-pickup-points/', views.campus_pickup_points, name='campus_pickup_points'),
    path('map/', views.map_view, name='map'),
    path('notifications/', views.notifications, name='notifications'),
]