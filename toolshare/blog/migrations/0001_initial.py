# Generated by Django 4.2.2 on 2023-08-01 12:59

import blog.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('category', models.CharField(choices=[('Carpentry work', 'Carpentry work'), ('Secondary work', 'Secondary work'), ('Finishing work', 'Finishing work'), ('Motoculture maintenance', 'Motoculture maintenance'), ('Green space maintenance', 'Green space maintenance'), ('Other', 'Other')], max_length=128)),
                ('location', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=2048)),
                ('availabalityStart', models.DateTimeField(default=django.utils.timezone.now, validators=[django.core.validators.MinValueValidator(limit_value=django.utils.timezone.now)])),
                ('availabalityEnd', models.DateTimeField(default=blog.models.oneDayHence, null=True, validators=[django.core.validators.MinValueValidator(limit_value=blog.models.oneDayHence)])),
                ('deposit', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('starred', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
