from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from authentication import forms
from authentication import models as authModels
from blog import models as blogModels
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from blog.scripts.parser import Parser
from blog.scripts.geocoderApi import Geocoder
from django.core.mail import EmailMessage
from datetime import date


# Create your views here.
class Home(LoginRequiredMixin, View):
    template_name = 'authentication/home.html'

    def get(self, request):
        return render(request, self.template_name)

class About(LoginRequiredMixin, View):
    template_name = 'authentication/about.html'

    def get(self, request, userID):
        return render(request, self.template_name)

class Contact(LoginRequiredMixin, View):
    template_name = 'authentication/contact.html'
    form_class = forms.ContactForm

    def get(self, request, userID):
        form = self.form_class()

        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID):
        user = authModels.User.objects.get(id=userID)
        form = self.form_class(request.POST)

        name = user.fullname
        emailFrom = user.email

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = "The user named " + name + " has sent you a message : \n" + form.cleaned_data['message'] + ".\nYou can reach him at this address : " + emailFrom
            recipientList = [settings.EMAIL_HOST_USER,]

            email = EmailMessage(subject, message, emailFrom, recipientList)
            email.send()
            return redirect(reverse('contact-success', kwargs={'userID': userID}))
        else:
            form = self.form_class()
        
            context = {
                'form': form,
            }
            return render(request, self.template_name, context=context)

class Publisher(LoginRequiredMixin, View):
    template_name = 'authentication/publisher.html'

    def get(self, request, userID):
        return render(request, self.template_name)

class Research(LoginRequiredMixin, View):
    template_name = 'authentication/research.html'

    def get(self, request, userID):
        tools = blogModels.Blog.objects.all()
        favorites = blogModels.Favorite.objects.all()
        contracts = blogModels.Contract.objects.all()

        for favorite in range(len(favorites)):
            for tool in range(len(tools)):
                if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                    tools[tool].match = True

        for tool in range(len(tools)):
            if tools[tool].availabalityStart <= date.today() <= tools[tool].availabalityEnd:
                tools[tool].availabality = True
            else:
                tools[tool].availabality = False

        for contract in range(len(contracts)):
            for tool in range(len(tools)):
                if contracts[contract].contractedBlog.id == tools[tool].id:
                    if date.today() > contracts[contract].endOfUse:
                        tools[tool].onContract = False
                        tools[tool].save()

        reverseToolsList = []
        for tool in reversed(range(len(tools))):
            reverseToolsList.append(tools[tool])

        if len(reverseToolsList) <= 4:
            tools = reverseToolsList[0:]
        
            context = {
                'tools': tools,
            }
            return render(request, self.template_name, context=context)
        elif len(reverseToolsList) > 4:
            tools = reverseToolsList[0:3]
            toolsCount = len(reverseToolsList)
        
            context = {
                'tools': tools,
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
                if allItems[tool].availabalityStart <= date.today() <= allItems[tool].availabalityEnd:
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
                if allTools[tool].availabalityStart <= date.today() <= allTools[tool].availabalityEnd:
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
                if allEquipments[tool].availabalityStart <= date.today() <= allEquipments[tool].availabalityEnd:
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

            reverseToolsList = []
            for tool in reversed(range(len(tools))):
                reverseToolsList.append(tools[tool])

            popularityScore = []
            for tool in range(len(reverseToolsList)):
                structure = {
                    'id': reverseToolsList[tool].id,
                    'popularity': reverseToolsList[tool].popularity,
                }
                popularityScore.append(structure)

            def get_popularity(popularityScore):
                return popularityScore.get('popularity')

            popularityScore.sort(key=get_popularity, reverse=True)

            popularTools = []
            for popularity in range(len(popularityScore)):
                popularTools.append(blogModels.Blog.objects.filter(id=popularityScore[popularity]['id']))

            mostPopularTools = []
            for tools in range(len(popularTools)):
                mostPopularTools.append(popularTools[tools][0])

            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(mostPopularTools)):
                    if mostPopularTools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        mostPopularTools[tool].match = True

            for tool in range(len(mostPopularTools)):
                if mostPopularTools[tool].availabalityStart <= date.today() <= mostPopularTools[tool].availabalityEnd:
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
                if bestTools[tool].availabalityStart <= date.today() <= bestTools[tool].availabalityEnd:
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
                messages.success(request, "Added to your Bag")

            tools = blogModels.Blog.objects.all()
            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True
                        tools[tool].save()

            for tool in range(len(tools)):
                if tools[tool].availabalityStart <= date.today() <= tools[tool].availabalityEnd:
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
                    userFavorites[favorite].blog.match = False
                    userFavorites[favorite].blog.save()
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
                    messages.info(request, "Removed from your Bag")
            
            tools = blogModels.Blog.objects.all()
            favorites = blogModels.Favorite.objects.all()

            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True
                        tools[tool].save()

            for tool in range(len(tools)):
                if tools[tool].availabalityStart <= date.today() <= tools[tool].availabalityEnd:
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
                        messages.warning(request, "Removed from your Personal Tools")
                    else:
                        blogModels.Blog.objects.filter(id=personalTools[tool].id)[0].image.delete()
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                        messages.warning(request, "Removed from your Personal Tools")

            tools = blogModels.Blog.objects.all()
            favorites = blogModels.Favorite.objects.all()
    
            for favorite in range(len(favorites)):
                for tool in range(len(tools)):
                    if tools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                        tools[tool].match = True

            for tool in range(len(tools)):
                if tools[tool].availabalityStart <= date.today() <= tools[tool].availabalityEnd:
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
  
        tools = blogModels.Blog.objects.all()
        contracts = blogModels.Contract.objects.all()

        for contract in range(len(contracts)):
            for tool in range(len(tools)):
                if contracts[contract].contractedBlog.id == tools[tool].id:
                    if date.today() > contracts[contract].endOfUse:
                        tools[tool].onContract = False
                        tools[tool].save()

        personalTools = blogModels.Blog.objects.filter(author=member.id)
        userApplicantContracts = blogModels.Contract.objects.filter(applicant=member)
        userSupplierContracts = blogModels.Contract.objects.filter(supplier=member)

        userApplicantContractStructure = []
        for contract in range(len(userApplicantContracts)):
            structure = {
                'applicant': member.username,
                'tool': userApplicantContracts[contract].contractedBlog,
                'supplier': userApplicantContracts[contract].supplier
            }
            userApplicantContractStructure.append(structure)

        userSupplierContractStructure = []
        for contract in range(len(userSupplierContracts)):
            structure = {
                'applicant': userSupplierContracts[contract].applicant,
                'tool': userSupplierContracts[contract].contractedBlog,
                'supplier': member.username,
            }
            userSupplierContractStructure.append(structure)

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
            'userApplicantContract': userApplicantContractStructure,
            'userSupplierContract': userSupplierContractStructure,
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
        elif "toolDetailsContract" in request.POST:
            print("1")
            toolID = int(request.POST.get("toolDetailsContract"))

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
        contracts = blogModels.Contract.objects.all()

        favorites = []
        for favorite in range(len(userFavorites)):
            favorites.append(userFavorites[favorite].blog)

        for tool in range(len(favorites)):
            if favorites[tool].availabalityStart <= date.today() <= favorites[tool].availabalityEnd:
                favorites[tool].availabality = True
            else:
                favorites[tool].availabality = False

        for contract in range(len(contracts)):
            for tool in range(len(favorites)):
                if contracts[contract].contractedBlog.id == favorites[tool].id:
                    if date.today() > contracts[contract].endOfUse:
                        favorites[tool].onContract = False
                        favorites[tool].save()

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

            toolSelected = blogModels.Blog.objects.get(id=favoriteId)
            toolSelected.popularity -= 1
            toolSelected.save()

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            for favorite in range(len(userFavorites)):
                if userFavorites[favorite].blog.id == favoriteId:
                    userFavorites[favorite].blog.match = False
                    userFavorites[favorite].blog.save()
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
                    messages.info(request, "Removed from your Bag")
            
            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            favorites = []
            for favorite in range(len(userFavorites)):
                favorites.append(userFavorites[favorite].blog)

            for tool in range(len(favorites)):
                if favorites[tool].availabalityStart <= date.today() <= favorites[tool].availabalityEnd:
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

        tools = blogModels.Blog.objects.all()
        contracts = blogModels.Contract.objects.all()

        for contract in range(len(contracts)):
            for tool in range(len(tools)):
                if contracts[contract].contractedBlog.id == tools[tool].id:
                    if date.today() > contracts[contract].endOfUse:
                        tools[tool].onContract = False
                        tools[tool].save()

        userApplicantContracts = blogModels.Contract.objects.filter(applicant=user)
        userSupplierContracts = blogModels.Contract.objects.filter(supplier=user)

        userApplicantContractStructure = []
        for contract in range(len(userApplicantContracts)):
            structure = {
                'applicant': user.username,
                'tool': userApplicantContracts[contract].contractedBlog,
                'supplier': userApplicantContracts[contract].supplier,
                'contractID': userApplicantContracts[contract].id
            }
            userApplicantContractStructure.append(structure)

        userSupplierContractStructure = []
        for contract in range(len(userSupplierContracts)):
            structure = {
                'applicant': userSupplierContracts[contract].applicant,
                'tool': userSupplierContracts[contract].contractedBlog,
                'supplier': user.username,
                'contractID': userSupplierContracts[contract].id
            }
            userSupplierContractStructure.append(structure)

        pathInfoUser = "/user/"+str(userID)+"/profile/"
        pathInfoMember = ""

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        reversePersonalToolList4 = reversePersonalToolList[0:4]

        context = {
            'user': user,
            'tools': reversePersonalToolList4,
            'userApplicantContract': userApplicantContractStructure,
            'userSupplierContract': userSupplierContractStructure,
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
        elif "toolDetailsContract" in request.POST:
            toolID = int(request.POST.get("toolDetailsContract"))

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
