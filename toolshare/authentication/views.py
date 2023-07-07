from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from authentication import forms
from authentication.models import User

# Create your views here.
def home(request):
    user = User.objects.all()
    return render(request, 'authentication/home.html', context={'user': user})

def research(request):
    return render(request, 'authentication/research.html')

def favorites(request):
    return render(request, 'authentication/favorites.html')

def profile(request):
    return render(request, 'authentication/profile.html')

def edit_profile(request):
    return render(request, 'authentication/edit_profile.html')

class Registration(View):
    template_name = 'authentication/registration.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})