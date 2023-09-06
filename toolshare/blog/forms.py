# blog/forms.py
from django import forms
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget
from . import models


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['name', 'image', 'category', 'description', 'location', 'availabalityStart', 'availabalityEnd', 'deposit']


class BorrowContractApplicant(forms.Form):
    fullname = forms.CharField(max_length=63)
    approval = forms.CharField(max_length=63)
    date = forms.DateField()
    postalAddress = forms.CharField(max_length=127)
    signature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'width': '350px', 'height': '150px'}))