# Generated by Django 4.2.2 on 2023-10-02 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_contract_applicantsignature_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='rating',
        ),
    ]
