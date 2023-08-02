from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from blog.models import Blog

# Create your models here.
class User(AbstractUser):
    fullname = models.fields.CharField(max_length=256, unique=True)
    phoneNumber = PhoneNumberField(blank=True)
    profilePicture = models.ImageField(default='userProfilePicture/defaultProfilePicture.png', upload_to='userProfilePicture')
    postalAddress = models.fields.CharField(max_length=256, null=True)
    personalTools = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    bio = models.fields.TextField(null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.username}'