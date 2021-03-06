# Generated by Django 2.2.5 on 2019-11-23 04:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.IntegerField(choices=[(0, 'Purchase'), (1, 'Borrow')], default=0),
        ),
    ]
