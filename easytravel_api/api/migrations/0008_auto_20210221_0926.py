# Generated by Django 3.1.2 on 2021-02-21 03:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210221_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_of_booking',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
