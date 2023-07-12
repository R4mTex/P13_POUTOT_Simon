from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from authentication import forms
from . import models
from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    user = models.User.objects.all()
    return render(request, 'authentication/home.html', context={'user': user})

def research(request):
    return render(request, 'authentication/research.html')

def favorites(request):
    return render(request, 'authentication/favorites.html')

def profile(request):
    return render(request, 'authentication/profile.html')

class editProfile(View):
    template_name = 'authentication/editProfile.html'
    form_class = forms.UploadProfilePhotoForm

    def get(self, request, id):
        form = self.form_class()
        user = models.User.objects.get(id=id)
        return render(request, 'authentication/editProfile.html', context={'form': form, 'user': user})

    def post(self, request, id):
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        user = models.User.objects.get(id=id)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'authentication/editProfile.html', context={'form': form, 'user': user})

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