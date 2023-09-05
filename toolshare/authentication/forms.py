from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django import forms
from authentication.models import User

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

class UpdateUserProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('fullname', 'username', 'email', 'phoneNumber', 'postalAddress', 'bio',)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
