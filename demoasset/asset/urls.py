from django.urls import path
from .views import register_employee, register_asset,custom_login_view

urlpatterns = [
    path('login/',custom_login_view, name='custom_login'),
    path('admin/register-employee/', register_employee, name='register_employee'),
    path('admin/register-asset/', register_asset, name='register_asset'),
]

'''path('admin/manage/',admin_manage_assets_and_employees, name='admin_manage'),
    path('manager/dashboard/', manager_dashboard_view, name='manager_dashboard'),
    path('employee/dashboard/', employee_dashboard_view, name='employee_dashboard'),
    path('admin/admin-dashboard/', admin_dashboard, name='admin_dashboard'),'''