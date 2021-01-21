from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# manager class


class MyAccountManager(BaseUserManager):

    # function to create user
    def create_user(self, email, username, name, phone, password=None):
        if not email:
            raise ValueError("User must have a email")
        if not username:
            raise ValueError('user must have a username')
        if not name:
            raise ValueError('user must have a name')
        if not phone:
            raise ValueError('user must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    # function to create super user
    def create_superuser(self, email, username, name, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            name=name,
            phone=phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

# custom user class


class Account(AbstractBaseUser):
    email = models.CharField(verbose_name='email', max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # setting required field for login and register
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'phone']

    # creating object for account manager class
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # function to create token for user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# model class to store registered vehicle


class RegisterVehicle(models.Model):
    brand = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    licenseNumber = models.CharField(max_length=50, blank=False, unique=True)
    category = models.CharField(max_length=20, blank=False)
    service = models.CharField(max_length=20, blank=False)
    description = models.CharField(max_length=500, blank=False)
    price = models.IntegerField(blank=False)
    vehicleImage = models.ImageField(default='Blank', blank=False)
    bluebookImage = models.ImageField(default='Blank', blank=False)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.model


class AssignDriver(models.Model):
    driverName = models.CharField(max_length=100, blank=False)
    driverAddress = models.CharField(max_length=100, blank=False)
    driverContact = models.CharField(max_length=20, blank=False, unique=True)
    licenseImage = models.ImageField(default='Blank', blank=False)
    vehicleId = models.OneToOneField(
        RegisterVehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.driverName
