# Generated by Django 3.0.3 on 2020-03-26 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20200327_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.AddField(
            model_name='geopoint',
            name='address',
            field=models.TextField(default=''),
        ),
    ]
