from rest_framework import serializers
from .models import CustomUser, Employee, Asset, MaintenanceRecord
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Return tokens and user role
        return {
            'access': str(access_token),
            'refresh': str(refresh),
            'role': ('superuser' if user.is_superuser else 'admin' if user.is_admin else 'manager' if user.is_manager else 'employee')
        }

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    maintenance_records = MaintenanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = ['name', 'description', 'price', 'purchase_date', 'maintenance_records', 'employee']


