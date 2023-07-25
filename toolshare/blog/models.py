from django.conf import settings
from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
class Blog(models.Model):
    name = models.CharField(max_length=128,)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    CATEGORY_CHOICES = [
        ("Carpentry work", "Carpentry work"),
        ("Secondary work", "Secondary work"),
        ("Finishing work", "Finishing work"),
        ("Motoculture maintenance", "Motoculture maintenance"),
        ("Green space maintenance", "Green space maintenance"),
        ("Other", "Other"),
    ]
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=128,)
    description = models.TextField(max_length=2048)
    availabalityStart = models.DateField()
    availabalityEnd = models.DateField(null=True,)
    deposit = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
