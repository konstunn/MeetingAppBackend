# Generated by Django 3.0.3 on 2020-03-30 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20200330_2251'),
        ('token_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='profiles', to='events.Category'),
        ),
    ]