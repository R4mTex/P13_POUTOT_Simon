# Generated by Django 4.2.2 on 2023-08-24 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]
