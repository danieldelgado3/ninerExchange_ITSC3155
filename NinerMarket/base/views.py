from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    # Add debug information
    print(f"Total listings: {listings.count()}")
    for listing in listings:
        print(f"Listing: {listing.name}, ID: {listing.id}, Seller: {listing.seller.username}")
    
    context = {'listings': listings, 'size': listings.count()}
    return render(request, 'base/home.html', context)

def login_view(request): #Login page view
    page = 'login'

    if request.user.is_authenticated:
        return redirect('base:Home') #If user is logged in, go to home

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            return redirect('signup')  #User login failed

    context = {'page': page} #Will be accessible from template (May need to adjust later?)
    return render(request, "base/loginPage.html", context)


@login_required
def settings(request): #Settings Page View
    return render(request, 'base/settings.html', {
        'user': request.user
    })

@login_required
def search(request): #Search Page View
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    listings = Listing.objects.filter(name__icontains=q) 

    condition = request.GET.get('condition')
    available = request.GET.get('available')
    sort = request.GET.get('sort')

    if condition:
        listings = listings.filter(condition=condition)

    if available == 'true':
        listings = listings.filter(available=True)
    elif available == 'false':
        listings = listings.filter(available=False)

    if sort == 'new':
        listings = listings.order_by('-created_at')
    elif sort == 'old':
        listings = listings.order_by('created_at')
    elif sort == 'price_asc':
        listings = listings.order_by('price')
    elif sort == 'price_desc':
        listings = listings.order_by('-price')

    context = {'listings': listings, 'size': listings.count()}
    return render(request, 'base/search.html', context)

def addItems(request):
    return render(request, 'base/addItems.html')


@login_required
# code only handles the image uploads for now
def addItemsToCloudinary(request): #AddItem Page View
    if request.method == 'POST':
        # Validate required fields
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        if not all([name, description, price]):
            messages.error(request, "All fields are required")
            return redirect('addItems')

        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        except ValueError:
            messages.error(request, "Please enter a valid price")
            return redirect('addItems')

        if not request.FILES:
            messages.error(request, "At least one image is required")
            return redirect('addItems')

        # create an empty list for image URLs
        image_urls = []

        # loop through all files and upload them to Cloudinary
        for i in range(1, 4):
            if f'image{i}' in request.FILES:
                try:
                    image = request.FILES[f'image{i}']
                    # Validate file type
                    if not image.content_type.startswith('image/'):
                        messages.error(request, f"File {i} must be an image")
                        return redirect('addItems')
                    
                    # Validate file size (max 5MB)
                    if image.size > 5 * 1024 * 1024:
                        messages.error(request, f"Image {i} is too large. Maximum size is 5MB")
                        return redirect('addItems')

                    # upload image to Cloudinary
                    upload_result = cloudinary.uploader.upload(
                        image,
                        folder="niner_market",  # Organize images in a folder
                        resource_type="image"
                    )
                    image_urls.append(upload_result['url'])
                except Exception as e:
                    messages.error(request, f"Error uploading image {i}: {str(e)}")
                    return redirect('addItems')

        # Fill remaining slots with None if less than 3 images
        while len(image_urls) < 3:
            image_urls.append(None)

        try:
            # Create the listing with the current user as seller
            listing = Listing.objects.create(
                name=name,
                description=description,
                price=price,
                image1_url=image_urls[0],
                image2_url=image_urls[1],
                image3_url=image_urls[2],
                seller=request.user
            )
            messages.success(request, f"Listing '{name}' created successfully!")
            return redirect('listing_detail', listing_id=listing.id)
        except Exception as e:
            messages.error(request, f"Error creating listing: {str(e)}")
            return redirect('addItems')
    else:
        messages.error(request, "Invalid request method")
        return redirect('addItems')

def signup_view(request):
    page = 'signup'

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
            print(form.errors)
            messages.error(request, "An error occured during registration")

    return render(request, 'base/register.html',{'form': form, 'universities': universities})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'base/listing_detail.html', {'listing': listing})

@login_required
def logout_view(request):
    logout(request)
    return redirect('Home')

@login_required
def profile(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        try:
            # Upload the image to Cloudinary
            image = request.FILES['profile_picture']
            
            # Validate file type
            if not image.content_type.startswith('image/'):
                messages.error(request, "File must be an image")
                return redirect('profile')
            
            # Validate file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                messages.error(request, "Image is too large. Maximum size is 5MB")
                return redirect('profile')
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                image,
                folder="niner_market/profile_pictures",
                resource_type="image"
            )
            
            # Update user's profile picture
            request.user.profile_picture = upload_result['url']
            request.user.save()
            
            messages.success(request, "Profile picture updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating profile picture: {str(e)}")
    
    # Get user's listings and conversations
    listings = request.user.listings.all()
    conversations = request.user.conversations.all().order_by('-updated_at')[:5]
    
    context = {
        'listings': listings,
        'conversations': conversations
    }
    
    return render(request, 'base/profile.html', context)

def campusPickup(request):
    locations = CampusLocation.objects.all()
    return render(request, 'base/campusPickup.html', {'locations': locations})

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'base/notifications.html')

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if the user owns the listing
    if listing.seller != request.user:
        messages.error(request, "You don't have permission to delete this listing.")
        return redirect('profile')
    
    try:
        # Delete images from Cloudinary
        if listing.image1_url:
            public_id = listing.image1_url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        if listing.image2_url:
            public_id = listing.image2_url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        if listing.image3_url:
            public_id = listing.image3_url.split('/')[-1].split('.')[0]
            cloudinary.uploader.destroy(public_id)
        
        # Delete the listing
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting listing: {str(e)}")
    
    return redirect('profile')



    
