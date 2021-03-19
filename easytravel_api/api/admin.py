from django.contrib import admin
from .models import Account, RegisterVehicle, AssignDriver, Booking, DeviceToken

admin.site.register(Account)
admin.site.register(RegisterVehicle)
admin.site.register(AssignDriver)
admin.site.register(Booking)
admin.site.register(DeviceToken)
