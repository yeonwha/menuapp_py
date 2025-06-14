# Generated by Django 4.2.21 on 2025-05-31 05:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('\x08(Main?|Dessert?|Drink?)\x08')])),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9 ]+$'), django.core.validators.MinLengthValidator(2)])),
                ('price', models.FloatField(validators=[django.core.validators.MaxValueValidator(999.99), django.core.validators.MinValueValidator(0.1)])),
                ('checked', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
