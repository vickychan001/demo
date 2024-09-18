from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='manager', limit_choices_to={'is_manager': True})
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

class Asset(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin', limit_choices_to={'is_admin': True})
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class MaintenanceRecord(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenance_records")
    details = models.TextField()
    date = models.DateField(auto_now_add=True)
