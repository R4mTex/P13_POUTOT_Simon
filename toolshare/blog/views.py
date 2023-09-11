from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms
from jsignature.utils import draw_signature
from authentication import models as authModels
from blog import models as blogModels
from blog.scripts.parser import Parser
from blog.scripts.geocoderApi import Geocoder
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from datetime import date
from django.template.loader import render_to_string
from PIL import Image, ImageTk
from io import BytesIO
from django.core.files import File


class editTool(LoginRequiredMixin, View):
    template_name = 'blog/editTool.html'

    def get (self, request, userID):
        blog_form = forms.BlogForm()
        user = authModels.User.objects.get(id=userID)

        context = {
            'blog_form': blog_form,
            'user': user,
        }
        return render(request, 'blog/editTool.html', context=context)
    
    def post (self, request, userID):
        blog_form = forms.BlogForm(request.POST, request.FILES)
        user = authModels.User.objects.get(id=userID)

        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            print(blog.image.path)
            print(type(blog.image.path))
            print(blog.image)
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

        pathPersonalToolsUser = "/user/"+str(userID)+"/personal-tools/"
        pathPersonalToolsMember = ""

        for tool in range(len(personalTools)):
            if personalTools[tool].availabalityStart <= date.today() <= personalTools[tool].availabalityEnd:
                personalTools[tool].availabality = True
            else:
                personalTools[tool].availabality = False

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        context = {
            'user': user,
            'tools': reversePersonalToolList,
            'pathPersonalToolsUser': pathPersonalToolsUser,
            'pathPersonalToolsMember': pathPersonalToolsMember,
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
                if personalTools[tool].availabalityStart <= date.today() <= personalTools[tool].availabalityEnd:
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

        pathPersonalToolsUser = ""
        pathPersonalToolsMember = "/user/"+str(userID)+"/member/"+str(memberID)+"/member-tools/"

        for tool in range(len(personalTools)):
            if personalTools[tool].availabalityStart <= date.today() <= personalTools[tool].availabalityEnd:
                personalTools[tool].availabality = True
            else:
                personalTools[tool].availabality = False

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        context = {
            'member': member,
            'tools': reversePersonalToolList,
            'pathPersonalToolsUser': pathPersonalToolsUser,
            'pathPersonalToolsMember': pathPersonalToolsMember,
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

            tools = blogModels.Blog.objects.filter(author=member)
            print(tools)

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
            
            tools = blogModels.Blog.objects.filter(author=member)

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
        elif "borrowRequest" in request.POST:
            return redirect(reverse('borrow-request-form', kwargs={'userID': userID, 'toolID': toolID}))


class borrowRequestForm(LoginRequiredMixin, View):
    template_name = 'authentication/borrowRequestForm.html'
    form_class = forms.ApplicantContractForm

    def get(self, request, userID, toolID):
        form = self.form_class()

        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, userID, toolID):
        user = authModels.User.objects.get(id=userID)
        member = blogModels.Blog.objects.get(id=toolID).author
        form = self.form_class(request.POST)
        #print("----------------------------------\n", self.form_class(request.POST))

        if form.is_valid():
            if form.cleaned_data.get('applicantName') != user.fullname:
                print("Here 1")
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context=context)
            elif Parser.scriptForParse(form.cleaned_data.get('applicantApproval')) != ['lu', 'approuve']:
                print("Here 2")
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context=context)
            elif form.cleaned_data.get('requestDate') != date.today():
                print("Here 3")
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context=context)
            elif form.cleaned_data.get('applicantPostalAddress') != user.postalAddress:
                print("Here 4")
                context = {
                    'form': form,
                }
                return render(request, self.template_name, context=context)
            else:
                applicantSignature = form.cleaned_data.get('applicantSignature')
                print("1 : ", applicantSignature)
                print("1 Type : ", type(applicantSignature))
                applicantSignatureFilePath = draw_signature(applicantSignature, as_file=True)
                print("2 : ", applicantSignatureFilePath)
                print("2 Type : ", type(applicantSignatureFilePath))

                newContract = form.save(commit=False)
                newContract.applicant = user
                newContract.applicantName = form.cleaned_data.get('applicantName')
                newContract.contractedBlog = blogModels.Blog.objects.get(id=toolID)
                newContract.applicantApproval = form.cleaned_data.get('applicantApproval')
                newContract.applicantPostalAddress = form.cleaned_data.get('applicantPostalAddress')
                newContract.applicantSignatureImage = applicantSignatureFilePath.replace("C:\\Users\\spout\\AppData\\Local\\Temp\\", '')
                print("3 : ", newContract.applicantSignatureImage)
                print("3 Type : ", type(newContract.applicantSignatureImage))
                newContract.requestDate = form.cleaned_data.get('requestDate')

                newContract.save()

                test = blogModels.Contract.objects.get(id=1).applicantSignatureImage
                test2 = blogModels.Blog.objects.get(id=1).image
                
                """
                print("4", blogModels.Contract.objects.all())
                for contract in range(len(blogModels.Contract.objects.all())):
                    print("4", blogModels.Contract.objects.all()[contract].applicantSignatureImage)
                    print("4.1", blogModels.Contract.objects.all()[contract].applicantSignatureImage.name)

                print("5", blogModels.Blog.objects.all())
                for blog in range(len(blogModels.Blog.objects.all())):
                    print("5", blogModels.Blog.objects.all()[blog].image)
                    print("5.1", blogModels.Blog.objects.all()[blog].image.name)
                """

                subject = "Borrow Request"
                emailFrom = settings.EMAIL_HOST_USER
                message = ""
                htmlContent = render_to_string('blog/consentToBorrowLink.html',)
                recipientList = [member.email,]

                email = EmailMultiAlternatives(subject, message, emailFrom, recipientList)
                email.attach_alternative(htmlContent, "text/html")

                email.send()

                context = {
                    'form': form,
                    'test': test,
                    'test2': test2,
                }
                return render(request, self.template_name, context=context)
        else:
            print("Here 6")
            context = {
                'form': form,
            }
            return render(request, self.template_name, context=context)

class consentToBorrowForm(LoginRequiredMixin, View):
    template_name = 'authentication/consentToBorrowForm.html'
    form_class = forms.SupplierContractForm

    def get(self, request):
        form = self.form_class()

        context = {
            'form': form,
        }
        return render(request, self.template_name, context=context)