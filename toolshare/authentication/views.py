from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'authentication/login.html')

def research(request):
    return render(request, 'authentication/research.html')

def favorites(request):
    return render(request, 'authentication/favorites.html')

def profile(request):
    return render(request, 'authentication/profile.html')

def edit_profile(request):
    return render(request, 'authentication/edit_profile.html')

def sign_up(request):
    return render(request, 'authentication/sign_up.html')