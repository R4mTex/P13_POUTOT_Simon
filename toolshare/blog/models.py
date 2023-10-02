from django.conf import settings
from django.db import models
from datetime import date, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from jsignature.fields import JSignatureField


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
    popularity = models.IntegerField(default=0)
    match = models.BooleanField(default=False)
    onContract = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_favorite', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.user}'
    

class SignatureModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_signature', on_delete=models.CASCADE)
    signature = JSignatureField()

    
class Contract(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applicant', on_delete=models.CASCADE)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier', on_delete=models.CASCADE, null=True)
    applicantName = models.CharField(max_length=128,)
    supplierName = models.CharField(max_length=128, null=True)
    contractedBlog = models.ForeignKey(Blog, related_name='contracted_tool', on_delete=models.CASCADE)
    applicantApproval = models.CharField(max_length=63)
    supplierApproval = models.CharField(max_length=63, null=True)
    applicantPostalAddress = models.CharField(max_length=127)
    supplierPostalAddress = models.CharField(max_length=127, null=True)
    applicantSignature =  models.ForeignKey(SignatureModel, related_name='applicant_signature', on_delete=models.CASCADE)
    supplierSignature =  models.ForeignKey(SignatureModel, related_name='supplier_signature', on_delete=models.CASCADE, null=True)
    requestDate = models.DateField(default=date.today,)
    approvalDate = models.DateField(default=date.today, null=True)
    startOfUse = models.DateField(default=date.today, validators=[MinValueValidator(limit_value=date.today)])
    endOfUse = models.DateField(validators=[MinValueValidator(limit_value=date.today)])
