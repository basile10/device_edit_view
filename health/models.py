
from django.db import models

# UserRole model for role management
class UserRole(models.Model):
    user_id = models.IntegerField(unique=True)  # Link to Django User id
    role = models.CharField(max_length=32)  # e.g., 'superadmin', 'user'

# Windows device and status models
class WindowsDevice(models.Model):
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=32)
    hostname = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    # online status is not editable, shown via related status

class WindowsDeviceStatus(models.Model):
    device = models.OneToOneField(WindowsDevice, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)

# Android device and status models
class AndroidDevice(models.Model):
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=32)
    hostname = models.CharField(max_length=64)
    location = models.CharField(max_length=128)

class AndroidDeviceStatus(models.Model):
    device = models.OneToOneField(AndroidDevice, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)
