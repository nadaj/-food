# Generated by Django 2.0.3 on 2018-04-16 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0014_product_stores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stores',
        ),
    ]
