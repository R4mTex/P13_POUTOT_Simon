from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from authentication import forms
from authentication import models as authModels
from blog import models as blogModels
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
class Home(LoginRequiredMixin, View):
    template_name = 'authentication/home.html'

    def get(self, request):
        return render(request, self.template_name)

@login_required
def research(request):
    return render(request, 'authentication/research.html')

@login_required
def favorites(request):
    return render(request, 'authentication/favorites.html')

class Profile(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'

    def get(self, request, id):
        user = authModels.User.objects.get(id=id)
        personalTools = blogModels.Blog.objects.filter(author=user.id)

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        reversePersonalToolList4 = reversePersonalToolList[0:4]

        context = {
            'user': user,
            'tools': reversePersonalToolList4,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, id):
        return render(request, self.template_name)

class editProfile(LoginRequiredMixin, View):
    template_name = 'authentication/editProfile.html'
    form_picture = forms.UploadProfilePictureForm
    form_profile = forms.SignupForm
    form_password = PasswordChangeForm

    def get(self, request, id):
        form_picture = self.form_picture()
        form_profile = self.form_profile()
        form_password = self.form_password(id)
        user = authModels.User.objects.get(id=id)

        context = {
            'form_picture': form_picture,
            'form_profile': form_profile,
            'form_password': form_password,
            'user': user,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        form_picture = self.form_picture(request.POST, request.FILES, instance=request.user)
        user = authModels.User.objects.get(id=id)
        if form_picture.is_valid():
            if user.profilePicture != 'userProfilePicture/defaultProfilePicture.png':
                user.profilePicture.delete()
                form_picture.save()
            else:
                form_picture.save()

            form_picture = self.form_picture()
            form_profile = self.form_profile()
            form_password = self.form_password(id)
            user = authModels.User.objects.get(id=id)

            context = {
                'form_picture': form_picture,
                'form_profile': form_profile,
                'form_password': form_password,
                'user': user,
            }
            return render(request, self.template_name, context=context)
        # if form profile
        # same picture = suppr
        

class Registration(View):
    template_name = 'authentication/registration.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        acceptedConditions = False
        context = {
            'form': form,
            'acceptedConditions': acceptedConditions,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class()
        if 'fullname' in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save()
                # auto-login user
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            context = {
                'form': form,
            }
            return render(request, self.template_name, context=context)
        elif 'accept' in request.POST:
            acceptedConditions = True
            context = {
                'form': form,
                'acceptedConditions': acceptedConditions,
            }
            return render(request, self.template_name, context=context)
        acceptedConditions = False
        context = {
            'form': form,
            'acceptedConditions': acceptedConditions,
        }
        return render(request, self.template_name, context=context)

"""
        user = authModels.User.objects.get(id=id)
        context = {
            'form_picture': self.form_picture,
            'form_profile': self.form_profile,
            'form_password': self.form_password,
            'user': user,
        }
        return render(request, self.template_name, context=context)
"""