# blog/forms.py
from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'category']


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'content', 'availabality', 'location']
