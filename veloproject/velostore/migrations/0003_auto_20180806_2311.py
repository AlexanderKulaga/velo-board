# Generated by Django 2.1 on 2018-08-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velostore', '0002_auto_20180806_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
