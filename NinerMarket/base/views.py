from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request): #Home Page View
    return HttpResponse('Home Page') 

def login(request):
    return render(request, 'base/loginPage.html')
