# Generated by Django 4.2.2 on 2023-09-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contract_applicantname_contract_suppliername'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='applicantSignature',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='supplierSignature',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]