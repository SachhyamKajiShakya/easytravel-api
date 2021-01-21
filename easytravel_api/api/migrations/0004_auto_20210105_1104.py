# Generated by Django 3.1.2 on 2021-01-05 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201211_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registervehicle',
            name='no_of_gears',
        ),
        migrations.RemoveField(
            model_name='registervehicle',
            name='no_of_seats',
        ),
        migrations.AddField(
            model_name='registervehicle',
            name='bluebookImage',
            field=models.ImageField(default='Blank', upload_to=''),
        ),
        migrations.AddField(
            model_name='registervehicle',
            name='vehicleImage',
            field=models.ImageField(default='Blank', upload_to=''),
        ),
    ]
