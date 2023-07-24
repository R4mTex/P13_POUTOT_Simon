import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from . import forms
from authentication import models as authModels
from blog import models as blogModels


@login_required
def blog_and_photo_upload(request, id):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    user = authModels.User.objects.get(id=id)
    if request.method == 'GET':
        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,
            'user': user
        }
        return render(request, 'blog/editTool.html', context=context)
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('profile')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
        'user': user,
    }
    return render(request, 'blog/editTool.html', context=context)


@login_required
def personalTools(request, id):
    user = authModels.User.objects.get(id=id)
    tools = blogModels.Blog.objects.filter(author=user.id)
    return render(request, 'blog/personalTools.html', {'user': user, 'tools': tools})