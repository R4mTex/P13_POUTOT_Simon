from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms
from authentication import models as authModels
from blog import models as blogModels
from django.utils import timezone


class editTool(LoginRequiredMixin, View):
    template_name = 'blog/editTool.html'

    def get (self, request, id):
        blog_form = forms.BlogForm()
        user = authModels.User.objects.get(id=id)

        context = {
            'blog_form': blog_form,
            'user': user
        }
        return render(request, 'blog/editTool.html', context=context)
    
    def post (self, request, id):
        blog_form = forms.BlogForm(request.POST, request.FILES)
        user = authModels.User.objects.get(id=id)

        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect(reverse('profile', kwargs={'id': id}))
        else:
            context = {
                'blog_form': blog_form,
                'user': user,
            }
            return render(request, self.template_name, context=context)


class personalTools(LoginRequiredMixin, View):
    template_name = 'blog/personalTools.html'

    def get(self, request, id):
        user = authModels.User.objects.get(id=id)
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
    
    def post(self, request, id):
        # submit = name=""
        tool_id = int(request.POST.get("submit"))

        user = authModels.User.objects.get(id=id)
        personalTools = blogModels.Blog.objects.filter(author=user.id)

        for tool in range(len(personalTools)):
            if personalTools[tool].id == tool_id:
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


