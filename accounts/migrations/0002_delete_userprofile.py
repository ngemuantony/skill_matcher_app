# Generated by Django 5.1.1 on 2024-10-06 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
