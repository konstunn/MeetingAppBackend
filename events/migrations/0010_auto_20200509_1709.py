# Generated by Django 3.0.3 on 2020-05-09 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_remove_event_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='decision',
            field=models.CharField(choices=[('ACCEPT', 'ACCEPT'), ('DECLINE', 'DECLINE'), ('NO_ANSWER', 'NO_ANSWER')], default='DECLINE', max_length=16),
        ),
    ]
