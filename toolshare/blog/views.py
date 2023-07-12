from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from . import forms
from . import models

# Create your views here.

@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST': 
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('photos')
    return render(request, 'blog/photoUpload.html', context={'form': form})


@login_required
def photos(request):
    photos = models.Photo.objects.all()
    return render(request, 'blog/photos.html', context={'photos': photos})