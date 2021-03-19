from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as django_logout
from django.conf import settings

# imports to be made from rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser

# imports to be made locally
from .serializers import UserRegistrationSerializer, RegisterVehicleSerializer, AssignDriverSerializer, UserUpdateSerializer
from .serializers import PhoneSerializer, OtpSerializer, ShortBookingSerializer, LongBookingSerializer, DeviceTokenSerializer
from .models import Account, RegisterVehicle, AssignDriver, Booking, DeviceToken
from .sms import verifications, verification_checks
from pyfcm import FCMNotification


# post method to enter the phone number and send otp
# @api_view(['POST'])
# @permission_classes([])
# def phone_verification(request):
#     if request.method == 'POST':
#         serializer = PhoneSerializer(data=request.data)
#         if serializer.is_valid():
#             request.session['phone'] = serializer.data['phone']
#             verification = verifications(
#                 request.session['phone'], 'sms')
#             print(request.session['phone'])
#         return Response({'phoneNumber': request.session['phone']})


# post method to check the entered otp code
# @api_view(['POST'])
# @permission_classes([])
# def otp_verification(request):
#     if request.method == 'POST':
#         serializer = OtpSerializer(data=request.data)
#         if serializer.is_valid():
#             print(serializer.data['otp'])
#             print(serializer.data['phoneNumber'])
#             verification = verification_checks(
#                 serializer.data['phoneNumber'], serializer.data['otp'])
#             if verification.status == 'approved':
#                 print(request.session['phoneNumber'])
#                 return Response({'status': verification.status})
#         return Response(serializer.data)


# method based api function to register user
@api_view(['POST'])
@permission_classes([])  # setting permission class to null
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# api put method to edit user data
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, user_id):
    user = Account.objects.get(id=user_id)
    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


# class based view to login user
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# class based view to logout user
class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based api method to register vehicle
@ api_view(['POST'])
# setting permission class to only authenticated user
@ permission_classes([IsAuthenticated])
def register_vehicle(request):
    vendor = request.user
    if request.method == 'POST':
        serializer = RegisterVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api method to read, update and delete vehicles
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_vehicles(request, vehicle_id):
    vehicle = RegisterVehicle.objects.get(id=vehicle_id)
    if request.method == "PUT":
        serializer = RegisterVehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        data = {}
        operation = RegisterVehicle.objects.get(id=vehicle_id).delete()
        if operation:
            data["success"] = "delete success"
        else:
            data["failure"] = "delete failure"
        return Response(data=data)


# get method to fetch vehicles with category short travel
@ api_view(['GET'])
@ permission_classes([IsAuthenticated])
def fetchShortVehicles(request):
    if request.method == 'GET':
        queryset = RegisterVehicle.objects.get(category='Short Travel')
        serializer = RegisterVehicleSerializer(queryset, many=True)
        return Response(serializer.data)


# fetch method to fetch vehicles with category long travel
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchLongVehicles(request):
    if request.method == 'GET':
        queryset = RegisterVehicle.objects.raw(
            "SELECT * FROM api_registervehicle WHERE category='Long Travel'")
        serializer = RegisterVehicleSerializer(queryset, many=True)
        return Response(serializer.data)


# function based api method to assign dirver
@api_view(['POST'])
# setting permission class to only authenticated user
@permission_classes([IsAuthenticated])
def assign_driver(request):
    registeredVehicleId = RegisterVehicle.objects.latest('id').pk
    registeredVehicle = RegisterVehicle.objects.get(id=registeredVehicleId)
    if request.method == 'POST':
        serializer = AssignDriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vehicleid=registeredVehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api method to read, update and delete driver
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manageDriver(request, id):
    driver = AssignDriver.objects.get(id=id)  # get driver of specific id
    if request.method == 'GET':
        queryset = AssignDriver.objects.filter(vehicleid=id)
        serializer = AssignDriverSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = AssignDriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        operation = driver.delete()
        data = {}
        if operation:
            data["success"] = "successful delete"
        else:
            data["failure"] = "delete unsuccessful"
        return Response(data=data)


# api method to enter vehicle for short bookings
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_shortbookings(request, vehicleid, driverid):
    assigned_driver = AssignDriver.objects.get(id=driverid)
    booked_vehicle = RegisterVehicle.objects.get(id=vehicleid)
    consumer = request.user
    if request.method == 'POST':
        serializer = ShortBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vehicle=booked_vehicle, driver=assigned_driver,
                            consumer=consumer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api method to enter vehicle for long booking
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_longbookings(request, vehicleid, driverid):
    assigned_driver = AssignDriver.objects.get(id=driverid)
    booked_vehicle = RegisterVehicle.objects.get(id=vehicleid)
    consumer = request.user
    if request.method == 'POST':
        serializer = LongBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vehicle=booked_vehicle, driver=assigned_driver,
                            consumer=consumer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post method to store device token for fcm
@api_view(['POST'])
@permission_classes([])
def store_device_token(request):
    consumer = request.user
    if request.method == 'POST':
        serializer = DeviceTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consumer_id=consumer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# POST method to send notification to the vendors
@api_view(['POST'])
@permission_classes([])
def send_notification(request):
    push_service = FCMNotification(
        api_key="AAAAKKogqpw:APA91bFr5bcuuMRpGGNiti-oQi8stniJvZ4k8JDoMJUQ5I1XsjzOJq7Fesu5ZkG6PitkMTT_YUZqyq-O1DtCYHaJMNhnohtzcVcMs7LzdQ2-z8cNVPIFryUmOmVLoBXS1kRk_JteIzWE")
    message_title = "message for vendor"
    message_body = "body for vendor"
    # data_message = {
    #     "driver_id":"",
    # }
    registration_id = "c9pbFgRfRDKSoEsHC-w6Qh:APA91bEnygeiC6R9yDKdlky-tZGEkcVH3aGolRJTXxREK685IZzwYg-zIAQtK2quihTkRE-b5mikniMYAA_umNUNm9nuV6-DFmvO65HqMQGzspDJSaUvxnSMpIz7eBZ9d3mOkK2pfKSK"
    push_service.notify_single_device(
        registration_id=registration_id, message_body=message_body, message_title=message_title)
    return Response(status=status.HTTP_410_GONE)


# POST method to send notificaitons to consumers
@api_view(['POST'])
@permission_classes([])
def send_consumernotification(request):
    push_service = FCMNotification(
        api_key="AAAAKKogqpw:APA91bFr5bcuuMRpGGNiti-oQi8stniJvZ4k8JDoMJUQ5I1XsjzOJq7Fesu5ZkG6PitkMTT_YUZqyq-O1DtCYHaJMNhnohtzcVcMs7LzdQ2-z8cNVPIFryUmOmVLoBXS1kRk_JteIzWE")
    message_title = "message for consumer"
    message_body = "body for consumer"
    registration_id = "c9pbFgRfRDKSoEsHC-w6Qh:APA91bEnygeiC6R9yDKdlky-tZGEkcVH3aGolRJTXxREK685IZzwYg-zIAQtK2quihTkRE-b5mikniMYAA_umNUNm9nuV6-DFmvO65HqMQGzspDJSaUvxnSMpIz7eBZ9d3mOkK2pfKSK"
    push_service.notify_single_device(
        registration_id=registration_id, message_body=message_body, message_title=message_title)
    return Response(status=status.HTTP_410_GONE)
