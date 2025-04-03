from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import dropbox
from django.conf import settings
from .models import Listing
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DROPBOX_OAUTH2_TOKEN = os.getenv('ACCESS_TOKEN') 


# Create your views here.
def home(request): #Home Page View
    return render(request, 'base/home.html')

def login_view(request): #Login page view
    page = 'login'

    if request.user.is_authenticated:
        return redirect('Home') #If user is logged in, go to home

    if request.method=="POST":
        username = request.POST.get('username').lower() #get username and password from form
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) # user object from form

        if user is not None: #if user exist
            login(request, user) #Call django login method
            return redirect('Home') #Redirect user to home page
        else:
            messages.error(request, 'Username or Password does not exist!') #User login failed

    context = {'page': page} #Will be accessible from template (May need to adjust later?)
    return render(request, "base/loginPage.html", context)


def settings(request): #Settings Page View
    return render(request, 'base/settings.html')

def addItems(request):
    return render(request, 'base/addItems.html')

def addItemsToDropbox(request): #AddItem Page View
    if request.method == 'POST' and request.FILES:
        dropboxObject = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price') 

        if 'image1' in request.FILES:
            image1 = request.FILES['image1']

            with image1.open('rb') as f:
                dropBoxPath = f'/media/{image1.name}'
                dropboxObject.files_upload(f.read(), dropBoxPath, mute = True)


        file = request.FILES
    return render(request, 'base/home.html') #need to fix this
