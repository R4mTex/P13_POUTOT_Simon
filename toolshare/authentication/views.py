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
        favorites = blogModels.Favorite.objects.all()

        for favorite in range(len(favorites)):
            for tool in range(len(tools)):
                if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                    tools[tool].match = True

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
        if "allItems" in request.POST:
            allItems = blogModels.Blog.objects.all()
            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(allItems)):
                    if allItems[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        allItems[tool].match = True

            for tool in range(len(allItems)):
                if allItems[tool].availabalityStart <= timezone.now() <= allItems[tool].availabalityEnd:
                    allItems[tool].availabality = True
                else:
                    allItems[tool].availabality = False

            reverseToolsList = []
            for tool in reversed(range(len(allItems))):
                reverseToolsList.append(allItems[tool])
            
            context = {
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)
        elif "allTools" in request.POST:
            allTools = blogModels.Blog.objects.exclude(category="Equipment")
            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(allTools)):
                    if allTools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        allTools[tool].match = True

            for tool in range(len(allTools)):
                if allTools[tool].availabalityStart <= timezone.now() <= allTools[tool].availabalityEnd:
                    allTools[tool].availabality = True
                else:
                    allTools[tool].availabality = False

            reverseToolsList = []
            for tool in reversed(range(len(allTools))):
                reverseToolsList.append(allTools[tool])
            
            context = {
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)
        elif "allEquipments" in request.POST:
            allEquipments = blogModels.Blog.objects.filter(category="Equipment")
            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(allEquipments)):
                    if allEquipments[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        allEquipments[tool].match = True

            for tool in range(len(allEquipments)):
                if allEquipments[tool].availabalityStart <= timezone.now() <= allEquipments[tool].availabalityEnd:
                    allEquipments[tool].availabality = True
                else:
                    allEquipments[tool].availabality = False

            reverseToolsList = []
            for tool in reversed(range(len(allEquipments))):
                reverseToolsList.append(allEquipments[tool])
            
            context = {
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)
        elif "mostPopular" in request.POST:
            tools = blogModels.Blog.objects.all()
            favorites = blogModels.Favorite.objects.all()

            popularityScore = []
            for tool in range(len(tools)):
                popularityScore.append(tools[tool].popularity)

            popularityScore.sort(reverse=True)

            mostPopularTools = []
            for popularity in range(len(popularityScore)):
                for tool in range(len(blogModels.Blog.objects.filter(popularity=popularityScore[popularity]))):
                    mostPopularTools.append(blogModels.Blog.objects.filter(popularity=popularityScore[popularity])[tool])

            for favorite in range(len(favorites)):
                for tool in range(len(mostPopularTools)):
                    if mostPopularTools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        mostPopularTools[tool].match = True

            for tool in range(len(mostPopularTools)):
                if mostPopularTools[tool].availabalityStart <= timezone.now() <= mostPopularTools[tool].availabalityEnd:
                    mostPopularTools[tool].availabality = True
                else:
                    mostPopularTools[tool].availabality = False

            context = {
                'tools': mostPopularTools,
            }
            return render(request, self.template_name, context=context)
        elif "bestRated" in request.POST:
            tools = blogModels.Blog.objects.all()
            
            scoreRate = []
            for tool in range(len(tools)):
                scoreRate.append(tools[tool].rating)

            scoreRate.sort(reverse=True)

            toolBestRated = []
            for score in range(len(scoreRate)):
                toolBestRated.append(blogModels.Blog.objects.filter(rating=scoreRate[score]))
            
            bestTools = []
            for value in range(len(toolBestRated)):
                bestTools.append(toolBestRated[value][0])

            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(bestTools)):
                    if bestTools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        bestTools[tool].match = True

            for tool in range(len(bestTools)):
                if bestTools[tool].availabalityStart <= timezone.now() <= bestTools[tool].availabalityEnd:
                    bestTools[tool].availabality = True
                else:
                    bestTools[tool].availabality = False

            context = {
                'tools': bestTools,
            }
            return render(request, self.template_name, context=context)
        elif "toolDetails" in request.POST:
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
        elif "addTool" in request.POST:
            toolID = int(request.POST.get("addTool"))

            toolSelected = blogModels.Blog.objects.get(id=toolID)
            toolSelected.popularity += 1
            toolSelected.save()

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            favoritesID = []
            for favorite in range(len(userFavorites)):
                favoritesID.append(userFavorites[favorite].blog.id)

            if toolSelected.id not in favoritesID:
                newFavorite = blogModels.Favorite()
                newFavorite.blog = toolSelected
                newFavorite.user = authModels.User.objects.get(id=userID)
                newFavorite.save()
                messages.success(request, "Added to your Favorites")

            tools = blogModels.Blog.objects.all()

            favorites = blogModels.Favorite.objects.all()
            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True

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
        elif "removeTool" in request.POST:
            favoriteId = int(request.POST.get("removeTool"))

            toolSelected = blogModels.Blog.objects.get(id=favoriteId)
            toolSelected.popularity -= 1
            toolSelected.save()

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            for favorite in range(len(userFavorites)):
                if userFavorites[favorite].blog.id == favoriteId:
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
                    messages.info(request, "Removed to your Favorites")
            
            tools = blogModels.Blog.objects.all()

            favorites = blogModels.Favorite.objects.all()
            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True

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
        elif "supprTool" in request.POST:
            toolID = int(request.POST.get("supprTool"))

            user = authModels.User.objects.get(id=userID)
            personalTools = blogModels.Blog.objects.filter(author=user.id)

            for tool in range(len(personalTools)):
                if personalTools[tool].id == toolID:
                    if personalTools[tool].image == "userPersonalToolPicture/defaultPersonalToolPicture.png":
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                        messages.warning(request, "Deleted to your Personal Tools")
                    else:
                        blogModels.Blog.objects.filter(id=personalTools[tool].id)[0].image.delete()
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                        messages.warning(request, "Deleted to your Personal Tools")

            tools = blogModels.Blog.objects.all()

            favorites = blogModels.Favorite.objects.all()
            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True

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
        elif "authorProfile" in request.POST:
            if int(request.POST.get("authorProfile")) == userID:
                return redirect(reverse('profile', kwargs={'userID': userID}))
            else:
                memberID = int(request.POST.get("authorProfile"))
                return redirect(reverse('member-profile', kwargs={'userID': userID, 'memberID': memberID}))
        

class memberProfile(LoginRequiredMixin, View):
    template_name = "authentication/profile.html"

    def get(self, request, userID, memberID):
        user = authModels.User.objects.get(id=userID)
        member = authModels.User.objects.get(id=memberID)
        personalTools = blogModels.Blog.objects.filter(author=member.id)

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        reversePersonalToolList4 = reversePersonalToolList[0:4]

        pathInfoUser = ""
        pathInfoMember = "/user/"+str(userID)+"/member/"+str(memberID)+"/member-profile/"

        context = {
            'user': user,
            'member': member,
            'tools': reversePersonalToolList4,
            'pathInfoUser': pathInfoUser,
            'pathInfoMember': pathInfoMember,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID, memberID):
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
        elif "showPersonalTools" in request.POST:
            return redirect(reverse('member-tools', kwargs={'userID': userID, 'memberID': memberID}))
        

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
        elif "removeTool" in request.POST:
            favoriteId = int(request.POST.get("removeTool"))

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

        pathInfoUser = "/user/"+str(userID)+"/profile/"
        pathInfoMember = ""

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        reversePersonalToolList4 = reversePersonalToolList[0:4]

        context = {
            'user': user,
            'tools': reversePersonalToolList4,
            'pathInfoUser': pathInfoUser,
            'pathInfoMember': pathInfoMember,
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
        elif "showPersonalTools" in request.POST:
            return redirect(reverse('personal-tools', kwargs={'userID': userID}))


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
