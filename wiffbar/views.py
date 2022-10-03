from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def collection(request):
    context = {

    }
    return render(request, 'collections.html', context)

def signup(request):
    return render(request,'sign-up.html')

def login(request):
    return render(request, 'login.html')