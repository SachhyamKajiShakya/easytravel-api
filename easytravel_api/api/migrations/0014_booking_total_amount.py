# Generated by Django 3.1.2 on 2021-04-05 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20210404_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
    ]
