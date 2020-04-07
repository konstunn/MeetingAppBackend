# Generated by Django 3.0.3 on 2020-03-29 20:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0019_auto_20200328_1520'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Invitation',
            new_name='Request',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='member',
            new_name='user',
        ),
    ]
