from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from django.core.validators import MinValueValidator


# Create your models here.
def oneDayHence():
    return date.today() + timedelta(days=1)


class Blog(models.Model):
    name = models.CharField(max_length=128,)
    image = models.ImageField(default='userPersonalToolPicture/defaultPersonalToolPicture.png', upload_to='userPersonalToolPicture')
    CATEGORY_CHOICES = [
        ("Carpentry work", "Carpentry work"),
        ("Secondary work", "Secondary work"),
        ("Finishing work", "Finishing work"),
        ("Motoculture maintenance", "Motoculture maintenance"),
        ("Green space maintenance", "Green space maintenance"),
        ("Equipment", "Equipment"),
        ("Other", "Other"),
    ]
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=128,)
    description = models.TextField(max_length=2048)
    availabalityStart = models.DateField(default=date.today, validators=[MinValueValidator(limit_value=date.today)])
    availabalityEnd = models.DateField(default=oneDayHence, validators=[MinValueValidator(limit_value=oneDayHence)])
    availabality = models.BooleanField(default=True)
    deposit = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    popularity = models.IntegerField(default=0)
    match = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.user}'

