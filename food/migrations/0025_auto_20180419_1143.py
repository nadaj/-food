# Generated by Django 2.0.3 on 2018-04-19 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0024_auto_20180419_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businesshours',
            name='state',
        ),
        migrations.DeleteModel(
            name='BusinessHours',
        ),
    ]
