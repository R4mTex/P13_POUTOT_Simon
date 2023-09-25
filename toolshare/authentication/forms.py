from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from authentication.models import User
from phonenumber_field.modelfields import PhoneNumberField


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('fullname', 'username', 'email', 'phoneNumber', 'postalAddress', 'bio',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UploadProfilePictureForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profilePicture',)


class UpdateUserProfile(forms.ModelForm):
    fullname = forms.CharField(max_length=256,)
    username = forms.CharField(max_length=256,)
    email = forms.EmailField()
    phoneNumber = PhoneNumberField()
    postalAddress = forms.CharField(max_length=256,)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), max_length=256)

    class Meta:
        model = User
        fields = ('fullname', 'username', 'email', 'phoneNumber', 'postalAddress', 'bio',)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=127)
    message = forms.CharField(widget=forms.Textarea)
