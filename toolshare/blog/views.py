from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from . import forms
from authentication import models as authModels
from blog import models as blogModels
from blog.scripts.parser import Parser
from blog.scripts.geocoderAPI import Geocoder
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from datetime import date
from django.template.loader import render_to_string
from blog.pdf import html2pdf


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
                        messages.warning(request, "Removed from your Personal Tools")
                    else:
                        blogModels.Blog.objects.filter(id=personalTools[tool].id)[0].image.delete()
                        blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                        messages.warning(request, "Removed from your Personal Tools")

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
                    'placeID': queryLocation['placeID'], }
            elif queryLocation['status'] != 'OK':
                data = {
                    'status': queryLocation['status'], }
            request.session['data'] = data
            return redirect(reverse('tool-details', kwargs={'userID': userID, 'toolID': toolID}))


class editTool(LoginRequiredMixin, View):
    template_name = 'blog/editTool.html'

    def get(self, request, userID):
        blog_form = forms.BlogForm()
        user = authModels.User.objects.get(id=userID)

        context = {
            'blog_form': blog_form,
            'user': user,
        }
        return render(request, 'blog/editTool.html', context=context)

    def post(self, request, userID):
        blog_form = forms.BlogForm(request.POST, request.FILES)
        user = authModels.User.objects.get(id=userID)

        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.name = Parser.removeUpperCase(blog_form.cleaned_data.get('name'))
            blog.category = Parser.removeUpperCase(blog_form.cleaned_data.get('category'))
            blog.author = request.user
            blog.save()
            return redirect(reverse('profile', kwargs={'userID': userID}))
        else:
            context = {
                'blog_form': blog_form,
                'user': user,
            }
            return render(request, self.template_name, context=context)


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
                    'placeID': queryLocation['placeID'], }
            elif queryLocation['status'] != 'OK':
                data = {
                    'status': queryLocation['status'], }
            request.session['data'] = data
            return redirect(reverse('tool-details', kwargs={'userID': userID, 'toolID': toolID}))
        elif "addTool" in request.POST:
            member = authModels.User.objects.get(id=memberID)
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
        elif "removeTool" in request.POST:
            member = authModels.User.objects.get(id=memberID)
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
            return redirect(reverse('research', kwargs={'userID': userID}))
        elif "borrowRequest" in request.POST:
            return redirect(reverse('borrow-request-form', kwargs={'userID': userID, 'toolID': toolID}))


class borrowRequestForm(LoginRequiredMixin, View):
    template_name = 'blog/borrowRequestForm.html'
    form_class = forms.ApplicantContractForm
    form_signature = forms.SignatureForm

    def get(self, request, userID, toolID):
        form = self.form_class()
        formSignature = self.form_signature()
        tool = blogModels.Blog.objects.get(id=toolID)

        context = {
            'form': form,
            'tool': tool,
            'formSignature': formSignature,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, userID, toolID):
        user = authModels.User.objects.get(id=userID)
        member = blogModels.Blog.objects.get(id=toolID).author
        tool = blogModels.Blog.objects.get(id=toolID)
        form = self.form_class(request.POST)
        formSignature = self.form_signature(request.POST or None)

        if form.is_valid() and formSignature.is_valid():
            applicantLocation = Parser.scriptForParse(form.cleaned_data.get('applicantPostalAddress'))
            statusApplicantLocation = Geocoder(applicantLocation).geocoderApiRequest()
            if form.cleaned_data.get('startOfUse') > tool.availabalityEnd:
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            elif form.cleaned_data.get('endOfUse') > tool.availabalityEnd:
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            elif form.cleaned_data.get('applicantName') != user.fullname:
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            elif Parser.scriptForParse(form.cleaned_data.get('applicantApproval')) != ['read', 'approved']:
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            elif form.cleaned_data.get('requestDate') != date.today():
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            elif statusApplicantLocation['status'] != "OK":
                context = {
                    'form': form,
                    'user': user,
                    'tool': tool,
                    'formSignature': formSignature,
                }
                return render(request, self.template_name, context=context)
            else:
                signature = formSignature.cleaned_data.get('signature')
                if signature:
                    newJSignatureModel = blogModels.SignatureModel()
                    newJSignatureModel.user = user
                    newJSignatureModel.signature = formSignature.cleaned_data.get('signature')
                    newJSignatureModel.save()

                newContract = blogModels.Contract()
                newContract.applicant = user
                newContract.supplier = member
                newContract.applicantName = form.cleaned_data.get('applicantName')
                newContract.contractedBlog = blogModels.Blog.objects.get(id=toolID)
                newContract.applicantApproval = form.cleaned_data.get('applicantApproval')
                newContract.applicantPostalAddress = form.cleaned_data.get('applicantPostalAddress')
                newContract.applicantSignature = blogModels.SignatureModel.objects.get(signature=formSignature.cleaned_data.get('signature'))
                newContract.requestDate = form.cleaned_data.get('requestDate')
                newContract.startOfUse = form.cleaned_data.get('startOfUse')
                newContract.endOfUse = form.cleaned_data.get('endOfUse')
                newContract.save()

                contracts = blogModels.Contract.objects.all()

                contractsID = []
                for contract in range(len(contracts)):
                    contractsID.append(contracts[contract].id)

                contractID = contractsID[-1]

                subject = "Borrow Request"
                emailFrom = settings.EMAIL_HOST_USER
                message = ""
                htmlContent = render_to_string('blog/consentToBorrowLink.html', {'userID': member.id, 'contractID': contractID})
                recipientList = [member.email,]

                email = EmailMultiAlternatives(subject, message, emailFrom, recipientList)
                email.attach_alternative(htmlContent, "text/html")

                email.send()
                return redirect(reverse('borrow-request-confirmation', kwargs={'userID': userID, 'toolID': toolID}))
        else:
            context = {
                'form': form,
                'user': user,
                'tool': tool,
                'formSignature': formSignature,
            }
            return render(request, self.template_name, context=context)


class borrowRequestConfirmation(LoginRequiredMixin, View):
    template_name = 'blog/borrowRequestConfirmation.html'

    def get(self, request, userID, toolID):
        return render(request, self.template_name)


class consentToBorrowForm(LoginRequiredMixin, View):
    template_name = 'blog/consentToBorrowForm.html'
    form_class = forms.SupplierContractForm
    form_signature = forms.SignatureForm

    def get(self, request, userID, contractID):
        form = self.form_class()
        formSignature = self.form_signature()
        tool = blogModels.Contract.objects.get(id=contractID).contractedBlog

        contract = blogModels.Contract.objects.get(id=contractID)
        applicantInfo = {
            'applicant': contract.applicant,
            'applicantName': contract.applicantName,
            'applicantApproval': contract.applicantApproval,
            'applicantSignature': contract.applicantSignature.signature,
            'requestDate': contract.requestDate,
            'startOfUse': contract.startOfUse,
            'endOfUse': contract.endOfUse,
        }
        context = {
            'form': form,
            'tool': tool,
            'formSignature': formSignature,
            'applicantInfo': applicantInfo,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, userID, contractID):
        user = authModels.User.objects.get(id=userID)
        contract = blogModels.Contract.objects.get(id=contractID)
        tool = blogModels.Contract.objects.get(id=contractID).contractedBlog
        form = self.form_class(request.POST)
        formSignature = self.form_signature(request.POST or None)

        if "consent" in request.POST:
            if form.is_valid() and formSignature.is_valid():
                supplierLocation = Parser.scriptForParse(form.cleaned_data.get('supplierPostalAddress'))
                statusSupplierLocation = Geocoder(supplierLocation).geocoderApiRequest()
                if form.cleaned_data.get('supplierName') != user.fullname:
                    applicantInfo = {
                        'applicant': contract.applicant,
                        'applicantName': contract.applicantName,
                        'applicantApproval': contract.applicantApproval,
                        'applicantSignature': contract.applicantSignature.signature,
                        'requestDate': contract.requestDate,
                        'startOfUse': contract.startOfUse,
                        'endOfUse': contract.endOfUse,
                    }
                    context = {
                        'form': form,
                        'tool': tool,
                        'formSignature': formSignature,
                        'applicantInfo': applicantInfo,
                    }
                    return render(request, self.template_name, context=context)
                elif Parser.scriptForParse(form.cleaned_data.get('supplierApproval')) != ['read', 'approved']:
                    applicantInfo = {
                        'applicant': contract.applicant,
                        'applicantName': contract.applicantName,
                        'applicantApproval': contract.applicantApproval,
                        'applicantSignature': contract.applicantSignature.signature,
                        'requestDate': contract.requestDate,
                        'startOfUse': contract.startOfUse,
                        'endOfUse': contract.endOfUse,
                    }
                    context = {
                        'form': form,
                        'tool': tool,
                        'formSignature': formSignature,
                        'applicantInfo': applicantInfo,
                    }
                    return render(request, self.template_name, context=context)
                elif form.cleaned_data.get('approvalDate') != date.today():
                    applicantInfo = {
                        'applicant': contract.applicant,
                        'applicantName': contract.applicantName,
                        'applicantApproval': contract.applicantApproval,
                        'applicantSignature': contract.applicantSignature.signature,
                        'requestDate': contract.requestDate,
                        'startOfUse': contract.startOfUse,
                        'endOfUse': contract.endOfUse,
                    }
                    context = {
                        'form': form,
                        'tool': tool,
                        'formSignature': formSignature,
                        'applicantInfo': applicantInfo,
                    }
                    return render(request, self.template_name, context=context)
                elif statusSupplierLocation['status'] != "OK":
                    applicantInfo = {
                        'applicant': contract.applicant,
                        'applicantName': contract.applicantName,
                        'applicantApproval': contract.applicantApproval,
                        'applicantSignature': contract.applicantSignature.signature,
                        'requestDate': contract.requestDate,
                        'startOfUse': contract.startOfUse,
                        'endOfUse': contract.endOfUse,
                    }
                    context = {
                        'form': form,
                        'tool': tool,
                        'formSignature': formSignature,
                        'applicantInfo': applicantInfo,
                    }
                    return render(request, self.template_name, context=context)
                else:
                    signature = formSignature.cleaned_data.get('signature')
                    if signature:
                        newJSignatureModel = blogModels.SignatureModel()
                        newJSignatureModel.user = user
                        newJSignatureModel.signature = formSignature.cleaned_data.get('signature')
                        newJSignatureModel.save()

                    contract = blogModels.Contract.objects.get(id=contractID)
                    contract.suppliertName = user.fullname
                    contract.supplierApproval = form.cleaned_data.get('supplierApproval')
                    contract.supplierPostalAddress = form.cleaned_data.get('supplierPostalAddress')
                    contract.supplierSignature = blogModels.SignatureModel.objects.get(signature=formSignature.cleaned_data.get('signature'))
                    contract.approvalDate = form.cleaned_data.get('approvalDate')
                    contract.save()

                    toolContracted = blogModels.Blog.objects.get(id=blogModels.Contract.objects.get(id=contractID).contractedBlog.id)
                    toolContracted.onContract = True
                    toolContracted.save()

                    contract = blogModels.Contract.objects.get(id=contractID)

                    subject = "Borrow Contract"
                    emailFrom = settings.EMAIL_HOST_USER
                    message = ""
                    htmlContent = render_to_string('blog/borrowContractLink.html', {'userID': userID, 'contractID': contractID})
                    recipientList = [contract.applicant.email, contract.supplier.email]

                    email = EmailMultiAlternatives(subject, message, emailFrom, recipientList)
                    email.attach_alternative(htmlContent, "text/html")

                    email.send()
                    return redirect(reverse('consent-to-borrow-confirmation', kwargs={'userID': userID, 'contractID': contractID}))
            else:
                applicantInfo = {
                    'applicant': contract.applicant,
                    'applicantName': contract.applicantName,
                    'applicantApproval': contract.applicantApproval,
                    'applicantSignature': contract.applicantSignature.signature,
                    'requestDate': contract.requestDate,
                    'startOfUse': contract.startOfUse,
                    'endOfUse': contract.endOfUse,
                }
                context = {
                    'form': form,
                    'tool': tool,
                    'formSignature': formSignature,
                    'applicantInfo': applicantInfo,
                }
                return render(request, self.template_name, context=context)
        elif "decline" in request.POST:
            contract = blogModels.Contract.objects.get(id=contractID)
            contract.delete()

            subject = "Borrow Request Declined"
            emailFrom = settings.EMAIL_HOST_USER
            message = "The request has been declined by the supplier"
            recipientList = [contract.applicant.email,]

            email = EmailMessage(subject, message, emailFrom, recipientList)

            email.send()
            return redirect(reverse('consent-to-borrow-confirmation', kwargs={'userID': userID, 'contractID': contractID}))


class consentToBorrowConfirmation(LoginRequiredMixin, View):
    template_name = 'blog/consentToBorrowConfirmation.html'

    def get(self, request, userID, contractID):
        if blogModels.Contract.objects.filter(id=contractID).exists():
            context = {
                'exists': True,
            }
            return render(request, self.template_name, context=context)
        else:
            context = {
                'exists': False,
            }
            return render(request, self.template_name, context=context)


class borrowContractPDF(LoginRequiredMixin, View):
    template_name = 'blog/borrowContract.html'

    def get(self, request, userID, contractID):
        user = authModels.User.objects.get(id=userID)
        contract = blogModels.Contract.objects.get(id=contractID)
        creationDate = date.today()
        contractInfo = {
            'applicant': contract.applicant,
            'supplier': contract.supplier,
            'creationDate': creationDate,
            'contractID': contract.id,
            'applicantName': contract.applicantName,
            'contractedBlog': contract.contractedBlog,
            'startOfUse': contract.startOfUse,
            'endOfUse': contract.endOfUse,
            'applicantApproval': contract.applicantApproval,
            'requestDate': contract.requestDate,
            'applicantPostalAddress': contract.applicantPostalAddress,
            'applicantSignature': contract.applicantSignature,
            'supplierName': contract.supplierName,
            'supplierApproval': contract.supplierApproval,
            'approvalDate': contract.approvalDate,
            'supplierPostalAddress': contract.supplierPostalAddress,
            'supplierSignature': contract.supplierSignature,
        }
        pdf = html2pdf(self.template_name, context_dict={'contractInfo': contractInfo, 'user': user})
        return HttpResponse(pdf, content_type="application/pdf")
