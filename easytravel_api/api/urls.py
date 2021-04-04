from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from api import views


app_name = 'api'

urlpatterns = [
    path('register/', views.user_registration, name='register'),
    path('updateuser/', views.updateUser, name='updateuser'),
    path('login/', views.CustomAuthToken.as_view(), name="login"),
    path('vehicle/', views.register_vehicle, name='vehicle'),
    path('driver/', views.assign_driver, name='driver'),
    path('vehicle/short', views.fetchShortVehicles, name='shortVehicle'),
    path('vehicle/long', views.fetchLongVehicles, name='longVehicle'),
    path('driver/<int:id>', views.manageDriver,
         name='driverdetails'),
    #     path('phoneNumber/', views.phone_verification, name='phoneNumber'),
    #     path('otp/', views.otp_verification, name='otpVerification'),
    path('shortbooking/<int:vehicleid>/<int:driverid>/',
         views.make_shortbookings, name='shortbooking'),
    path('longbooking/<int:vehicleid>/<int:driverid>/',
         views.make_longbookings, name='longbooking'),
    path('updatelongbookings/<int:booking_id>',
         views.update_longbookings, name='updatelongbookings'),
    path('updateshortbookings/<int:booking_id>', views.update_shortbookings,
         name='updateshortbookings'),
    path('fcm/<int:vehicle_id>', views.send_notification, name="fcm"),
    path('storedevicetoken/', views.store_device_token, name='storedevicetoken'),
    path('updatedevicetoken', views.updateDeviceToken, name='updatedevicetoken'),
    path('managevehicles/<int:vehicle_id>',
         views.manage_vehicles, name='managevehicles'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('getbooking/<int:booking_id>', views.getBooking, name='getBooking'),
    path('confirmmessage/<int:booking_id>',
         views.send_confirmnotification, name='confirmmessage'),
    path('cancelmessage/<int:booking_id>',
         views.send_cancelnotification, name='cancelmessage'),
    path('pastbookings',
         views.getPastBookings, name='pastbooking'),
    path('futurebookings', views.getFutureBookings, name='cancelmessage'),
    path('postedvehicles', views.getPostedvehicles, name='postedvehicles'),
    path('getuserdata', views.getUserData, name='getuserdata'),
    path('updatepassword', views.UpdatePassword.as_view(), name='updatepassword'),
    path('cancelbooking/<int:booking_id>',
         views.sendvendor_cancelmessage, name='cancelbooking'),
    path('postbookingrequest', views.postedVehicleRequest,
         name='postbookingrequest'),
]
