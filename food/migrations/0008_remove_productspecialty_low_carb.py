# Generated by Django 2.0.3 on 2018-04-11 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20180411_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productspecialty',
            name='low_carb',
        ),
    ]
