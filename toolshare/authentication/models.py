from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    fullname = models.fields.CharField(max_length=256, unique=True)
    email = models.fields.EmailField(max_length=256, unique=True)
    phoneNumber = PhoneNumberField(blank=True)
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.fullname}'