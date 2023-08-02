from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('fullname', 'username', 'email', 'phoneNumber', 'postalAddress', 'bio')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class UploadProfilePictureForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['profilePicture',]