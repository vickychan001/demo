from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Employee, Asset
from .serializers import EmployeeSerializer, AssetSerializer, CustomTokenObtainPairSerializer
from rest_framework import status
from django.http import HttpResponseForbidden
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view(['POST'])
def custom_login_view(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_manage_assets_and_employees(request):
    user = request.user
    if user.is_admin and user.is_superuser:
        if request.method == 'GET':
            employees = Employee.objects.all()
            assets = Asset.objects.all()
            employee_serializer = EmployeeSerializer(employees, many=True)
            asset_serializer = AssetSerializer(assets, many=True)
            return Response({'employees': employee_serializer.data, 'assets': asset_serializer.data}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = request.data
            if 'employee' in data:
                employee_serializer = EmployeeSerializer(data=data['employee'])
                if employee_serializer.is_valid():
                    employee_serializer.save()
                    return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
                return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif 'asset' in data:
                asset_serializer = AssetSerializer(data=data['asset'])
                if asset_serializer.is_valid():
                    asset_serializer.save()
                    return Response(asset_serializer.data, status=status.HTTP_201_CREATED)
                return Response(asset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    if not request.user.is_admin and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this resource")

    employees = Employee.objects.all()
    assets = Asset.objects.all()
    
    employee_serializer = EmployeeSerializer(employees, many=True)
    asset_serializer = AssetSerializer(assets, many=True)

    return Response({
        'employees': employee_serializer.data,
        'assets': asset_serializer.data
    })'''

@api_view(['POST'])
# @permission_classes([IsAdminUser])
def register_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_asset(request):
    '''if not request.user.is_admin and request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this resource")'''

    serializer = AssetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''@api_view(['GET'])
@permission_classes([IsAdminUser])
def manager_dashboard_view(request):
    user = request.user
    if user.is_manager:
        employees = Employee.objects.filter(manager=user)
        assets = Asset.objects.filter(employee__in=employees)
        employee_serializer = EmployeeSerializer(employees, many=True)
        asset_serializer = AssetSerializer(assets, many=True)
        return Response({'employees': employee_serializer.data, 'assets': asset_serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def employee_dashboard_view(request):
    user = request.user
    if user.is_employee:
        employee = Employee.objects.get(user=user)
        assets = Asset.objects.filter(employee=employee)
        employee_serializer = EmployeeSerializer(employee)
        asset_serializer = AssetSerializer(assets, many=True)
        if request.method == 'GET':
            return Response({'employee': employee_serializer.data, 'assets': asset_serializer.data}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = request.data
            asset_id = data.get('asset_id')
            maintenance_details = data.get('maintenance_details')
            asset = Asset.objects.get(id=asset_id, employee=employee)
            asset.maintenance_records.create(details=maintenance_details)
            return Response({'message': 'Maintenance record updated successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)'''
