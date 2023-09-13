# Generated by Django 4.2.2 on 2023-09-13 09:51

import blog.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jsignature.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(default='userPersonalToolPicture/defaultPersonalToolPicture.png', upload_to='userPersonalToolPicture')),
                ('category', models.CharField(choices=[('Carpentry work', 'Carpentry work'), ('Secondary work', 'Secondary work'), ('Finishing work', 'Finishing work'), ('Motoculture maintenance', 'Motoculture maintenance'), ('Green space maintenance', 'Green space maintenance'), ('Equipment', 'Equipment'), ('Other', 'Other')], max_length=128)),
                ('location', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=2048)),
                ('availabalityStart', models.DateField(default=datetime.date.today, validators=[django.core.validators.MinValueValidator(limit_value=datetime.date.today)])),
                ('availabalityEnd', models.DateField(default=blog.models.oneDayHence, validators=[django.core.validators.MinValueValidator(limit_value=blog.models.oneDayHence)])),
                ('availabality', models.BooleanField(default=True)),
                ('deposit', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField(default=0.0)),
                ('popularity', models.IntegerField(default=0)),
                ('match', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SignatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', jsignature.fields.JSignatureField()),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='blog.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicantName', models.CharField(max_length=128)),
                ('supplierName', models.CharField(blank=True, max_length=128)),
                ('applicantApproval', models.CharField(max_length=63)),
                ('supplierApproval', models.CharField(blank=True, max_length=63)),
                ('applicantPostalAddress', models.CharField(max_length=127)),
                ('supplierPostalAddress', models.CharField(blank=True, max_length=127)),
                ('requestDate', models.DateField(default=datetime.date.today)),
                ('approvalDate', models.DateField(null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL)),
                ('applicantSignatureImage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_signature', to='blog.signaturemodel')),
                ('contractedBlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracted_tool', to='blog.blog')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to=settings.AUTH_USER_MODEL)),
                ('supplierSignatureImage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_signature', to='blog.signaturemodel')),
            ],
        ),
    ]
