from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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


def settings(request): #Home Page View
    return render(request, 'base/settings.html')
