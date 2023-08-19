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
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from blog.scripts.parser import Parser
from blog.scripts.geocoderApi import Geocoder

# Create your views here.
class Home(LoginRequiredMixin, View):
    template_name = 'authentication/home.html'

    def get(self, request):
        return render(request, self.template_name)

class Research(LoginRequiredMixin, View):
    template_name = 'authentication/research.html'

    def get(self, request, userID):
        tools = blogModels.Blog.objects.all()

        for tool in range(len(tools)):
            if tools[tool].availabalityStart <= timezone.now() <= tools[tool].availabalityEnd:
                tools[tool].availabality = True
            else:
                tools[tool].availabality = False

        reverseToolsList = []
        for tool in reversed(range(len(tools))):
            reverseToolsList.append(tools[tool])
        
        context = {
            'tools': reverseToolsList,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID):
        if "toolDetails" in request.POST:
            toolID = int(request.POST.get("toolDetails"))

            tool = blogModels.Blog.objects.get(id=toolID)
            toolLocationParsed = Parser.scriptForParse(tool.location)

            geocoderRequest = Geocoder(toolLocationParsed).geocoderApiRequest()
            queryLocation = Geocoder(geocoderRequest).dataRequest()

            if queryLocation['status'] == 'OK':
                data = {
                    'status': queryLocation['status'],
                    'longName': queryLocation['longName'],
                    'lat': queryLocation['lat'],
                    'lng': queryLocation['lng'],
                    'placeID': queryLocation['placeID'],
                    }
            elif queryLocation['status'] != 'OK':
                data = {
                    'status': queryLocation['status'],
                    }
            request.session['data'] = data
            return redirect(reverse('tool-details', kwargs={'userID': userID, 'toolID': toolID}))
        else:
            toolID = int(request.POST.get("submit"))

            toolSelected = blogModels.Blog.objects.get(id=toolID)
            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            favoritesID = []
            for favorite in range(len(userFavorites)):
                favoritesID.append(userFavorites[favorite].blog.id)

            if toolSelected.id not in favoritesID:
                newFavorite = blogModels.Favorite()
                newFavorite.blog = toolSelected
                newFavorite.user = authModels.User.objects.get(id=userID)
                newFavorite.save()
                messages.success(request, "Tool saved !")
            else:
                messages.warning(request, "Tool already saved !")

            tools = blogModels.Blog.objects.all()

            for tool in range(len(tools)):
                if tools[tool].availabalityStart <= timezone.now() <= tools[tool].availabalityEnd:
                    tools[tool].availabality = True
                else:
                    tools[tool].availabality = False

            reverseToolsList = []
            for tool in reversed(range(len(tools))):
                reverseToolsList.append(tools[tool])
            
            context = {
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)


class Favorites(LoginRequiredMixin, View):
    template_name = 'authentication/favorites.html'

    def get(self, request, userID):
        userFavorites = blogModels.Favorite.objects.filter(user=userID)

        favorites = []
        for favorite in range(len(userFavorites)):
            favorites.append(userFavorites[favorite].blog)

        for tool in range(len(favorites)):
            if favorites[tool].availabalityStart <= timezone.now() <= favorites[tool].availabalityEnd:
                favorites[tool].availabality = True
            else:
                favorites[tool].availabality = False

        reverseFavoritesList = []
        for tool in reversed(range(len(favorites))):
            reverseFavoritesList.append(favorites[tool])
        
        context = {
            'tools': reverseFavoritesList,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID):
        if "toolDetails" in request.POST:
            toolID = int(request.POST.get("toolDetails"))

            tool = blogModels.Blog.objects.get(id=toolID)
            toolLocationParsed = Parser.scriptForParse(tool.location)

            geocoderRequest = Geocoder(toolLocationParsed).geocoderApiRequest()
            queryLocation = Geocoder(geocoderRequest).dataRequest()

            if queryLocation['status'] == 'OK':
                data = {
                    'status': queryLocation['status'],
                    'longName': queryLocation['longName'],
                    'lat': queryLocation['lat'],
                    'lng': queryLocation['lng'],
                    'placeID': queryLocation['placeID'],
                    }
            elif queryLocation['status'] != 'OK':
                data = {
                    'status': queryLocation['status'],
                    }
            request.session['data'] = data
            return redirect(reverse('tool-details', kwargs={'userID': userID, 'toolID': toolID}))
        else:
            favoriteId = int(request.POST.get("submit"))

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            for favorite in range(len(userFavorites)):
                if userFavorites[favorite].blog.id == favoriteId:
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
            
            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            favorites = []
            for favorite in range(len(userFavorites)):
                favorites.append(userFavorites[favorite].blog)

            for tool in range(len(favorites)):
                if favorites[tool].availabalityStart <= timezone.now() <= favorites[tool].availabalityEnd:
                    favorites[tool].availabality = True
                else:
                    favorites[tool].availabality = False

            reverseFavoritesList = []
            for tool in reversed(range(len(favorites))):
                reverseFavoritesList.append(favorites[tool])
            
            context = {
                'tools': reverseFavoritesList,
            }
            return render(request, self.template_name, context=context)
        

class Profile(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'

    def get(self, request, userID):
        user = authModels.User.objects.get(id=userID)
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
    
    def post(self, request, userID):
        return render(request, self.template_name)

class editProfile(LoginRequiredMixin, View):
    template_name = 'authentication/editProfile.html'
    form_picture = forms.UploadProfilePictureForm
    form_profile = forms.UpdateUserProfile
    form_password = PasswordChangeForm

    def get(self, request, userID):
        user = authModels.User.objects.get(id=userID)
        form_picture = self.form_picture()
        form_profile = self.form_profile(instance=user)
        form_password = self.form_password(id)

        context = {
            'user': user,
            'form_picture': form_picture,
            'form_profile': form_profile,
            'form_password': form_password,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, userID):
        user = authModels.User.objects.get(id=userID)
        if 'profilePicture' in request.POST:
            form_picture = self.form_picture(request.POST, request.FILES, instance=request.user)
            if form_picture.is_valid():
                if user.profilePicture == 'userProfilePicture/defaultProfilePicture.png' or user.profilePicture == form_picture.cleaned_data['profilePicture']:
                    form_picture.save()
                else:
                    user.profilePicture.delete()
                    form_picture.save()
                
                user = authModels.User.objects.get(id=userID)
                form_picture = self.form_picture()
                form_profile = self.form_profile(instance=user)
                form_password = self.form_password(id)

                context = {
                    'user': user,
                    'form_picture': form_picture,
                    'form_profile': form_profile,
                    'form_password': form_password,
                }
                return render(request, self.template_name, context=context)
            else:
                user = authModels.User.objects.get(id=userID)
                form_picture = self.form_picture()
                form_profile = self.form_profile(instance=user)
                form_password = self.form_password(userID)

                context = {
                    'user': user,
                    'form_picture': form_picture,
                    'form_profile': form_profile,
                    'form_password': form_password,
                }
                return render(request, self.template_name, context=context)
        if 'updateUserProfile' in request.POST:
            form_profile = self.form_profile(request.POST)
            if form_profile.is_valid():
                print("yes")
                user = authModels.User.objects.get(id=userID)
                form_picture = self.form_picture()
                form_profile = self.form_profile(instance=request.user)
                form_password = self.form_password(userID)

                context = {
                    'user': user,
                    'form_picture': form_picture,
                    'form_profile': form_profile,
                    'form_password': form_password,
                }
                return render(request, self.template_name, context=context)
            else:
                print('Error')
                print(form_profile.errors)
                user = authModels.User.objects.get(id=userID)
                form_picture = self.form_picture()
                form_profile = self.form_profile(instance=request.user)
                form_password = self.form_password(userID)

                context = {
                    'user': user,
                    'form_picture': form_picture,
                    'form_profile': form_profile,
                    'form_password': form_password,
                }
                return render(request, self.template_name, context=context)
            

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