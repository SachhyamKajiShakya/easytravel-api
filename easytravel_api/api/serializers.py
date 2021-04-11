from rest_framework import serializers
from .models import Account, RegisterVehicle, AssignDriver, Booking, DeviceToken


# creating serializer class for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'username', 'name', 'phone',
                  'password']

 # creating model serializer to update user data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'name', 'username', 'phone']


# creating model serialzier to update user password
class UpdatePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(required=True)
    newpassword = serializers.CharField(required=True)


# serializer class for vehicle registration
class RegisterVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterVehicle
        fields = ['id', 'brand', 'model', 'licenseNumber', 'category',
                  'service', 'description', 'price', 'vehicleImage', 'bluebookImage']


# serializer class for updating vehicle
class UpdateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterVehicle
        fields = ['brand', 'model', 'licenseNumber',
                  'category', 'service', 'description', 'price']


# model serialzier for posting driver
class AssignDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignDriver
        fields = ['id', 'driverName', 'driverAddress',
                  'driverContact', 'licenseImage']


# model serializer for storing user phone number
class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()


# model serializer for storing the OTP verification code
class OtpSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    otp = serializers.CharField()


# model serialzier for posting short booking vehicles
class ShortBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'pick_up_date', 'pick_up_time', 'pick_up_district', 'pick_up_city',
                  'pick_up_street', 'destination_district', 'destination_city', 'destination_street', 'total_amount']


# model serializer for posting long booking vehicles
class LongBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'pick_up_province', 'number_of_days', 'pick_up_district', 'pick_up_city', 'pick_up_street', 'pick_up_date', 'pick_up_time', 'destination_province',
                  'destination_district', 'destination_city', 'destination_street', 'total_amount']


# model serialzier for posting short booking vehicles
class UpdateShortBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pick_up_date', 'pick_up_time', 'pick_up_district', 'pick_up_city',
                  'pick_up_street', 'destination_district', 'destination_city', 'destination_street']

# model serializer for posting long booking vehicles


class UpdateLongBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pick_up_province', 'number_of_days', 'pick_up_district', 'pick_up_city', 'pick_up_street', 'pick_up_date', 'pick_up_time', 'destination_province',
                  'destination_district', 'destination_city', 'destination_street']


# model serializer for storing device registration token
class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['device_token']


# model serializer for bookings
class GetBookingSerializer(serializers.ModelSerializer):

    customer_name = serializers.SerializerMethodField()
    customer_contact = serializers.SerializerMethodField()
    driver_name = serializers.SerializerMethodField()
    driver_contact = serializers.SerializerMethodField()
    vehicle_brand = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    vehicle_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'customer_name', 'customer_contact', 'driver_name', 'driver_contact', 'vehicle_brand', 'vehicle_model', 'vehicle_price', 'pick_up_date', 'pick_up_time', 'pick_up_province', 'pick_up_district', 'pick_up_city', 'pick_up_street',
                  'destination_province', 'destination_district', 'destination_city', 'destination_street', 'number_of_days', 'status', 'image', 'total_amount']

    def get_customer_name(self, obj):
        f_customer_name = obj.consumer.name
        return f_customer_name

    def get_customer_contact(self, obj):
        f_customer_contact = obj.consumer.phone
        return f_customer_contact

    def get_driver_name(self, obj):
        f_driver_name = obj.driver.driverName
        return f_driver_name

    def get_driver_contact(self, obj):
        f_driver_contact = obj.driver.driverContact
        return f_driver_contact

    def get_vehicle_brand(self, obj):
        f_vehicle_brand = obj.vehicle.brand
        return f_vehicle_brand

    def get_vehicle_model(self, obj):
        f_vehicle_model = obj.vehicle.model
        return f_vehicle_model

    def get_vehicle_price(self, obj):
        f_vehicle_price = obj.vehicle.price
        print(f_vehicle_price)
        return f_vehicle_price

    def get_image(self, obj):
        return 'http://192.168.100.67:8000/media/{}'.format(obj.vehicle.vehicleImage)


# model serializer for posted vehicle
class PostedvehicleRequest(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

# model serialzier for reset password


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['password']
