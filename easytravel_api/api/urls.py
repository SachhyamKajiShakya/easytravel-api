from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import user_registration, register_vehicle, CustomAuthToken, assign_driver
from .views import fetchShortVehicles, fetchLongVehicles, fetchDriverDetails, make_shortbookings, make_longbookings, send_notification
from .views import store_device_token
# phone_verification, otp_verification


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
    # path('phoneNumber/', phone_verification, name='phoneNumber'),
    # path('otp/', otp_verification, name='otpVerification'),
    path('shortbooking/<int:vehicleid>/<int:driverid>/',
         make_shortbookings, name='shortbooking'),
    path('longbooking/<int:vehicleid>/<int:driverid>/',
         make_longbookings, name='longbooking'),
    path('fcm/', send_notification, name="fcm"),
    path('storedevicetoken/', store_device_token, name='storedevicetoken'),
]
