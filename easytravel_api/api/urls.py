from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .views import user_registration, register_vehicle, CustomAuthToken, assign_driver
from .views import fetchShortVehicles, fetchLongVehicles, manageDriver, make_shortbookings, make_longbookings, send_notification
from .views import store_device_token, manage_vehicles, LogoutView, updateUser, getBooking, send_consumernotification
# phone_verification, otp_verification


app_name = 'api'

urlpatterns = [
    path('register/', user_registration, name='register'),
    path('updateuser/<int:user_id>', updateUser, name='updateuser'),
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('vehicle/', register_vehicle, name='vehicle'),
    path('driver/', assign_driver, name='driver'),
    path('vehicle/short', fetchShortVehicles, name='shortVehicle'),
    path('vehicle/long', fetchLongVehicles, name='longVehicle'),
    path('driver/<int:id>', manageDriver,
         name='driverdetails'),
    # path('phoneNumber/', phone_verification, name='phoneNumber'),
    # path('otp/', otp_verification, name='otpVerification'),
    path('shortbooking/<int:vehicleid>/<int:driverid>/',
         make_shortbookings, name='shortbooking'),
    path('longbooking/<int:vehicleid>/<int:driverid>/',
         make_longbookings, name='longbooking'),
    path('fcm/<int:vehicle_id>', send_notification, name="fcm"),
    path('storedevicetoken/', store_device_token, name='storedevicetoken'),
    path('managevehicles/<int:vehicle_id>',
         manage_vehicles, name='managevehicles'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getbooking/<int:booking_id>', getBooking, name='getBooking'),
    path('confirmmessage/<int:booking_id>',
         send_consumernotification, name='confirmmessage'),
]
