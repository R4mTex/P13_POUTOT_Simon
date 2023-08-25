from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms
from authentication import models as authModels
from blog import models as blogModels
from django.utils import timezone
from blog.scripts.parser import Parser
from blog.scripts.geocoderApi import Geocoder
from django.contrib import messages


class editTool(LoginRequiredMixin, View):
    template_name = 'blog/editTool.html'

    def get (self, request, userID):
        blog_form = forms.BlogForm()
        user = authModels.User.objects.get(id=userID)

        context = {
            'blog_form': blog_form,
            'user': user
        }
        return render(request, 'blog/editTool.html', context=context)
    
    def post (self, request, userID):
        blog_form = forms.BlogForm(request.POST, request.FILES)
        user = authModels.User.objects.get(id=userID)

        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect(reverse('profile', kwargs={'userID': userID}))
        else:
            context = {
                'blog_form': blog_form,
                'user': user,
            }
            return render(request, self.template_name, context=context)


class personalTools(LoginRequiredMixin, View):
    template_name = 'blog/personalTools.html'

    def get(self, request, userID):
        user = authModels.User.objects.get(id=userID)
        personalTools = blogModels.Blog.objects.filter(author=user.id)

        users = authModels.User.objects.all()
        usersFullname = []
        for fullname in range(len(users)):
            usersFullname.append(users[fullname].fullname)

        if "Fictive" not in usersFullname:
            authModels.User.objects.create(fullname="Fictive",
                                            username="Fic",
                                            phoneNumber="+33680111133",
                                            email="Fictive@Fic.com",)

        member = authModels.User.objects.get(fullname="Fictive")

        for tool in range(len(personalTools)):
            if personalTools[tool].availabalityStart <= timezone.now() <= personalTools[tool].availabalityEnd:
                personalTools[tool].availabality = True
            else:
                personalTools[tool].availabality = False

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        context = {
            'user': user,
            'member': member,
            'tools': reversePersonalToolList,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID):
        if "supprTool" in request.POST:
            toolID = int(request.POST.get("supprTool"))

            user = authModels.User.objects.get(id=userID)
            personalTools = blogModels.Blog.objects.filter(author=user.id)

            for tool in range(len(personalTools)):
                if personalTools[tool].id == toolID:
                    if personalTools[tool].image == "userPersonalToolPicture/defaultPersonalToolPicture.png":
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                    else:
                        blogModels.Blog.objects.filter(id=personalTools[tool].id)[0].image.delete()
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()

            personalTools = blogModels.Blog.objects.filter(author=user.id)

            for tool in range(len(personalTools)):
                if personalTools[tool].availabalityStart <= timezone.now() <= personalTools[tool].availabalityEnd:
                    personalTools[tool].availabality = True
                else:
                    personalTools[tool].availabality = False

            reversePersonalToolList = []
            for tool in reversed(range(len(personalTools))):
                reversePersonalToolList.append(personalTools[tool])

            context = {
                'user': user,
                'tools': reversePersonalToolList,
            }
            return render(request, self.template_name, context=context)
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
        

class memberTools(LoginRequiredMixin, View):
    template_name = 'blog/personalTools.html'

    def get(self, request, userID, memberID):
        member = authModels.User.objects.get(id=memberID)
        personalTools = blogModels.Blog.objects.filter(author=member.id)

        favorites = blogModels.Favorite.objects.all()

        for favorite in range(len(favorites)):
            for tool in range(len(personalTools)):
                if personalTools[tool].id == favorites[favorite].blog.id and request.user.username == favorites[favorite].user.username:
                    personalTools[tool].match = True

        for tool in range(len(personalTools)):
            if personalTools[tool].availabalityStart <= timezone.now() <= personalTools[tool].availabalityEnd:
                personalTools[tool].availabality = True
            else:
                personalTools[tool].availabality = False

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        context = {
            'member': member,
            'tools': reversePersonalToolList,
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
        elif "addTool" in request.POST:
            member = authModels.User.objects.get(id=memberID)
            toolID = int(request.POST.get("addTool"))

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
                'member': member,
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)
        elif "removeTool" in request.POST:
            member = authModels.User.objects.get(id=memberID)
            favoriteId = int(request.POST.get("removeTool"))

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            for favorite in range(len(userFavorites)):
                if userFavorites[favorite].blog.id == favoriteId:
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
            
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
                'member': member,
                'tools': reverseToolsList,
            }
            return render(request, self.template_name, context=context)
        elif "authorProfile" in request.POST:
            authorID = int(request.POST.get("authorProfile"))
            return redirect(reverse('member-profile', kwargs={'userID': userID, 'memberID': authorID}))
    

class toolDetails(LoginRequiredMixin, View):
    template_name = "blog/toolDetails.html"

    def get(self, request, userID, toolID):
        tool = blogModels.Blog.objects.get(id=toolID)
        favorite = blogModels.Favorite.objects.filter(blog=tool)

        favoriteUsers = []
        for users in range(len(favorite)):
            favoriteUsers.append(favorite[users].user)

        context = {
            'tool': tool,
            'favoriteUsers': favoriteUsers,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID, toolID):
        if "addTool" in request.POST:
            toolID = int(request.POST.get("addTool"))

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
        elif "removeTool" in request.POST:
            favoriteId = int(request.POST.get("removeTool"))

            userFavorites = blogModels.Favorite.objects.filter(user=userID)

            for favorite in range(len(userFavorites)):
                if userFavorites[favorite].blog.id == favoriteId:
                    blogModels.Favorite.objects.filter(id=userFavorites[favorite].id).delete()
        elif "supprTool" in request.POST:
            toolID = int(request.POST.get("supprTool"))

            user = authModels.User.objects.get(id=userID)
            personalTools = blogModels.Blog.objects.filter(author=user.id)

            for tool in range(len(personalTools)):
                if personalTools[tool].id == toolID:
                    if personalTools[tool].image == "userPersonalToolPicture/defaultPersonalToolPicture.png":
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                    else:
                        blogModels.Blog.objects.filter(id=personalTools[tool].id)[0].image.delete()
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()