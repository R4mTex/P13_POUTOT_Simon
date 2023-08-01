# blog/forms.py
from django import forms
from . import models


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['name', 'image', 'category', 'description', 'location', 'availabalityStart', 'availabalityEnd', 'deposit']
