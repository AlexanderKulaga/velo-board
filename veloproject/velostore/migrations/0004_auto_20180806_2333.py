# Generated by Django 2.1 on 2018-08-06 20:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velostore', '0003_auto_20180806_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mark',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='post',
            name='phone_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Формат: '+999999999'. Допускается меньше 15 цифр", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]