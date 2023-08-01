from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


# Create your models here.
def oneDayHence():
    return timezone.now() + timezone.timedelta(days=1)


class Blog(models.Model):
    name = models.CharField(max_length=128,)
    image = models.ImageField(default='userPersonalToolPicture/defaultPersonalToolPicture.png', upload_to='userPersonalToolPicture')
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
    availabalityStart = models.DateTimeField(default=timezone.now, validators=[MinValueValidator(limit_value=timezone.now)])
    availabalityEnd = models.DateTimeField(default=oneDayHence, validators=[MinValueValidator(limit_value=oneDayHence)], null=True,)
    deposit = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
