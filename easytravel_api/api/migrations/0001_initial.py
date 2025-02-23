# Generated by Django 3.1.2 on 2021-02-09 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('licenseNumber', models.CharField(max_length=50, unique=True)),
                ('category', models.CharField(max_length=20)),
                ('service', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=500)),
                ('price', models.IntegerField()),
                ('vehicleImage', models.ImageField(default='Blank', upload_to='')),
                ('bluebookImage', models.ImageField(default='Blank', upload_to='')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssignDriver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driverName', models.CharField(max_length=100)),
                ('driverAddress', models.CharField(max_length=100)),
                ('driverContact', models.CharField(max_length=20, unique=True)),
                ('licenseImage', models.ImageField(default='Blank', upload_to='')),
                ('vehicleId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.registervehicle')),
            ],
        ),
    ]
