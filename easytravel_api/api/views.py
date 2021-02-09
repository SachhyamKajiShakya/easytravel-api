from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings

# imports to be made from rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

# imports to be made locally
from .serializers import UserRegistrationSerializer, RegisterVehicleSerializer, AssignDriverSerializer
from .models import Account, RegisterVehicle, AssignDriver


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


# class based view to login user
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# function based api method to register vehicle
@api_view(['POST', 'GET'])
# setting permission class to only authenticated user
@permission_classes([IsAuthenticated])
def register_vehicle(request):
    vendor = request.user
    if request.method == 'POST':
        serializer = RegisterVehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get method to fetch vehicles with category short travel
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchShortVehicles(request):
    if request.method == 'GET':
        queryset = RegisterVehicle.objects.raw(
            "SELECT * FROM api_registervehicle WHERE category='Short Travel'")
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchDriverDetails(request, id):
    if request.method == 'GET':
        queryset = AssignDriver.objects.filter(vehicleid=id)
        serializer = AssignDriverSerializer(queryset, many=True)
        return Response(serializer.data)
