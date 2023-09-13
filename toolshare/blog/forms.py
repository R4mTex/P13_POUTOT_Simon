# blog/forms.py
from django import forms
from . import models
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['name', 'image', 'category', 'description', 'location', 'availabalityStart', 'availabalityEnd', 'deposit']


class SignatureForm(forms.Form):
    signature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'width': '350px', 'height': '150px'}))


class ApplicantContractForm(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = "__all__"
        exclude = ('applicant', 'supplier', 'supplierName', 'contractedBlog', 'supplierApproval', 'supplierPostalAddress', 'applicantSignatureImage', 'supplierSignatureImage', 'approvalDate')


class SupplierContractForm(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = "__all__"
        exclude = ('applicant', 'supplier', 'applicantName', 'contractedBlog', 'applicantApproval', 'applicantPostalAddress', 'applicantSignatureImage', 'supplierSignatureImage', 'requestDate')
