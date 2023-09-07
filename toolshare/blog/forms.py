# blog/forms.py
from django import forms
from . import models
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['name', 'image', 'category', 'description', 'location', 'availabalityStart', 'availabalityEnd', 'deposit']


class ContractForm(forms.ModelForm):
    applicantSignature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'width': '350px', 'height': '150px'}))
    supplierSignature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'width': '350px', 'height': '150px'}))

    class Meta:
        model = models.Contract
        fields = "__all__"
