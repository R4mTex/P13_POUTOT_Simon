from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'authentication/login.html')

def research(request):
    return render(request, 'authentication/research.html')