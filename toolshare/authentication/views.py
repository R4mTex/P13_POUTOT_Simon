from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from authentication import forms
from . import models
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
@login_required
def home(request):
    user = models.User.objects.all()
    return render(request, 'authentication/home.html', context={'user': user})

@login_required
def research(request):
    return render(request, 'authentication/research.html')

@login_required
def favorites(request):
    return render(request, 'authentication/favorites.html')

class Profile(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'

    def get(self, request):
        return render(request, 'authentication/profile.html')
    
    def post(self, request):
        return render(request, 'authentication/profile.html')

class editProfile(LoginRequiredMixin, View):
    template_name = 'authentication/editProfile.html'
    form_class = forms.UploadProfilePhotoForm
    form_password = PasswordChangeForm

    def get(self, request, id):
        form = self.form_class()
        form_password = self.form_password(id)
        user = models.User.objects.get(id=id)
        print(user.profilePicture)
        return render(request, self.template_name, context={'form': form, 'form_password': form_password, 'user': user})

    def post(self, request, id):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        user = models.User.objects.get(id=id)
        if form.is_valid():
            if user.profilePicture != 'userProfilePicture/defaultProfilePicture.png':
                user.profilePicture.delete()
                form.save()
            else:
                form.save()

            form = self.form_class()
            form_password = self.form_password(id)

            user = models.User.objects.get(id=id)

            return render(request, self.template_name, context={'form': form, 'form_password': form_password, 'user': user})
        return render(request, self.template_name, context={'form': form, 'form_password': form_password, 'user': user})

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
