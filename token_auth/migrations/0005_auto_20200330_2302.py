# Generated by Django 3.0.3 on 2020-03-30 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20200330_2251'),
        ('token_auth', '0004_auto_20200330_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='categories',
            field=models.ManyToManyField(related_name='profiles', to='events.Category'),
        ),
    ]