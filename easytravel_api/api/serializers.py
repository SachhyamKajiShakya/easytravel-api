from rest_framework import serializers
from .models import Account, RegisterVehicle, AssignDriver

# creating serializer class for user registration


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'name',
                  'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # overwriting save function to create user
    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

    # show error if passwords do not match
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'passwords msut match'})
        account.set_password(password)
        account.save()
        return account

# serializer class for vehicle registration


class RegisterVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterVehicle
        fields = ['id', 'brand', 'model', 'licenseNumber', 'category',
                  'service', 'description', 'price', 'vehicleImage', 'bluebookImage']


class AssignDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignDriver
        fields = ['id', 'driverName', 'driverAddress',
                  'driverContact', 'licenseImage']
