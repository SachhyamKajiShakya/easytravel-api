from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from api import views
# from .views import user_registration, register_vehicle, CustomAuthToken, assign_driver
# from .views import fetchShortVehicles, fetchLongVehicles, manageDriver, make_shortbookings, make_longbookings, send_notification
# from .views import store_device_token, manage_vehicles, LogoutView, updateUser, getBooking, send_confirmnotification
# phone_verification, otp_verification


app_name = 'api'

urlpatterns = [
    path('register/', views.user_registration, name='register'),
    path('updateuser/<int:user_id>', views.updateUser, name='updateuser'),
    path('login/', views.CustomAuthToken.as_view(), name="login"),
    path('vehicle/', views.register_vehicle, name='vehicle'),
    path('driver/', views.assign_driver, name='driver'),
    path('vehicle/short', views.fetchShortVehicles, name='shortVehicle'),
    path('vehicle/long', views.fetchLongVehicles, name='longVehicle'),
    path('driver/<int:id>', views.manageDriver,
         name='driverdetails'),
    # path('phoneNumber/', views.phone_verification, name='phoneNumber'),
    # path('otp/', views.otp_verification, name='otpVerification'),
    path('shortbooking/<int:vehicleid>/<int:driverid>/',
         views.make_shortbookings, name='shortbooking'),
    path('longbooking/<int:vehicleid>/<int:driverid>/',
         views.make_longbookings, name='longbooking'),
    path('fcm/<int:vehicle_id>', views.send_notification, name="fcm"),
    path('storedevicetoken/', views.store_device_token, name='storedevicetoken'),
    path('managevehicles/<int:vehicle_id>',
         views.manage_vehicles, name='managevehicles'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('getbooking/<int:booking_id>', views.getBooking, name='getBooking'),
    path('confirmmessage/<int:booking_id>',
         views.send_confirmnotification, name='confirmmessage'),
    path('cancelmessage/<int:booking_id>',
         views.send_cancelnotification, name='cancelmessage'),
]
