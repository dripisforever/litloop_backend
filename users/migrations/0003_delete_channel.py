# Generated by Django 4.2.4 on 2023-11-12 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_channel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Channel',
        ),
    ]