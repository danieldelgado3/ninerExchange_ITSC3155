from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .models import Listing, Universities
from .models import CampusLocation
from dotenv import load_dotenv, find_dotenv
import cloudinary
import cloudinary.uploader
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


# Create your views here.
@login_required
def home(request): #Home Page View
    listings = Listing.objects.all()
    context = {'listings': listings, 'size': listings.count()}

    return render(request, 'base/home.html', context)

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
            return redirect('signup')  #User login failed

    context = {'page': page} #Will be accessible from template (May need to adjust later?)
    return render(request, "base/loginPage.html", context)


@login_required
def settings(request): #Settings Page View
    return render(request, 'base/settings.html')

@login_required
def search(request): #Search Page View
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    listings = Listing.objects.filter(name__icontains=q) 

    context = {'listings': listings, 'size': listings.count()}
    return render(request, 'base/search.html', context)

def addItems(request):
    return render(request, 'base/addItems.html')


@login_required
# code only handles the image uploads for now
def addItemsToCloudinary(request): #AddItem Page View
    if request.method == 'POST' and request.FILES:
        # retrieve the form data (name, description, price)
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price') 

        # create an empty list for image URLs, each image upload to cloudinary will return 
        # a url that we store in this list to manipulate the listings
        image_urls = []

        # loop through all files and upload them to Cloudinary
        for i in range(1, 4):
            if f'image{i}' in request.FILES:
                image = request.FILES[f'image{i}']
                
                # upload image to Cloudinary and store the url thats returned here
                upload_result = cloudinary.uploader.upload(image)
                
                # get the URL of the uploaded image and adds it to the list
                image_urls.append(upload_result['url'])

        while len(image_urls) < 3: #None images if user does not upload three images
            image_urls.append(None)

        Listing.objects.create(
            name = name, description = description, price = price, image1_url=image_urls[0],
            image2_url=image_urls[1],  image3_url=image_urls[2],
        )

        return redirect('Home')

@login_required
def campusPickup(request):
    locations = CampusLocation.objects.all()
    return render(request, 'base/campusPickup.html', {'locations': locations})

def signup_view(request):
    universities = Universities.objects.all()
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.name.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "An error occured during registration")

    return render(request, 'base/register.html', {'universities': universities})

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'base/listing_detail.html', {'listing': listing})

@login_required
def logout_view(request):
    logout(request)
    return redirect('Home')



    
