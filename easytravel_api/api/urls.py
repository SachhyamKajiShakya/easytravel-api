from django.urls import path
from .views import user_registration, register_vehicle, CustomAuthToken, assign_driver
from .views import fetchShortVehicles, fetchLongVehicles, fetchDriverDetails
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('vehicle/', register_vehicle, name='vehicle'),
    path('driver/', assign_driver, name='driver'),
    path('vehicle/short', fetchShortVehicles, name='shortVehicle'),
    path('vehicle/long', fetchLongVehicles, name='longVehicle'),
    path('driver/<int:id>', fetchDriverDetails,
         name='driverdetails'),
]
