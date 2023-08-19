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
    

class ToolDetails(LoginRequiredMixin, View):
    template_name = "blog/toolDetails.html"

    def get(self, request, userID, toolID):
        tool = blogModels.Blog.objects.get(id=toolID)

        context = {
            'tool': tool,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID, toolID):
        return render(request, self.template_name)
