# Generated by Django 2.0.3 on 2018-04-15 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_store_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stores',
            field=models.ManyToManyField(through='food.ProductStore', to='food.Store'),
        ),
    ]
