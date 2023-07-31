from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms
from authentication import models as authModels
from blog import models as blogModels
import datetime
import pytz


class editTool(LoginRequiredMixin, View):
    template_name = 'blog/editTool.html'
    dateTimeNow = datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime("%Y-%m-%d %H:%M:%S"+"+02:00")

    def get (self, request, id):
        blog_form = forms.BlogForm()
        photo_form = forms.PhotoForm()
        user = authModels.User.objects.get(id=id)
        print(self.dateTimeNow)

        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,
            'user': user
        }
        return render(request, 'blog/editTool.html', context=context)
    
    def post (self, request, id):
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        user = authModels.User.objects.get(id=id)

        if all([blog_form.is_valid(), photo_form.is_valid()]):
            availabalityStart = str(blog_form.cleaned_data['availabalityStart'])
            availabalityEnd = str(blog_form.cleaned_data['availabalityEnd'])
            if self.dateTimeNow <= availabalityStart < availabalityEnd:
                print('True', self.dateTimeNow, availabalityStart, availabalityEnd)
                photo = photo_form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                blog = blog_form.save(commit=False)
                blog.author = request.user
                blog.photo = photo
                blog.save()
                return redirect(reverse('profile', kwargs={'id': id}))
            else:
                print('False', self.dateTimeNow, availabalityStart, availabalityEnd)
                context = {
                    'blog_form': blog_form,
                    'photo_form': photo_form,
                    'user': user,
                }
                return render(request, self.template_name, context=context)
        else:
            context = {
                'blog_form': blog_form,
                'photo_form': photo_form,
                'user': user,
            }
            return render(request, self.template_name, context=context)


class personalTools(LoginRequiredMixin, View):
    template_name = 'blog/personalTools.html'

    def get(self, request, id):
        user = authModels.User.objects.get(id=id)
        personalTools = blogModels.Blog.objects.filter(author=user.id)

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
                blogModels.Blog.objects.filter(id=personalTools[tool].id).delete()
                blogModels.Photo.objects.filter(image=personalTools[tool].photo.image)[0].image.delete()

        personalTools = blogModels.Blog.objects.filter(author=user.id)

        reversePersonalToolList = []
        for tool in reversed(range(len(personalTools))):
            reversePersonalToolList.append(personalTools[tool])

        context = {
            'user': user,
            'tools': reversePersonalToolList,
        }
        return render(request, self.template_name, context=context)


