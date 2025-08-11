

import sys
import os
import django

def seed():
    from health.models import WindowsDevice, WindowsDeviceStatus, AndroidDevice, AndroidDeviceStatus
    from django.contrib.auth.models import User
    from health.models import UserRole

    # Create a superadmin user if not exists
    user, created = User.objects.get_or_create(username='superadmin', defaults={'is_superuser': True, 'is_staff': True})
    # Always set password and superuser/staff status
    user.is_superuser = True
    user.is_staff = True
    user.set_password('admin123')
    user.save()
    # Always ensure UserRole is set for this user
    UserRole.objects.update_or_create(user_id=user.id, defaults={'role': 'superadmin'})

    # Windows devices
    try:
        win1 = WindowsDevice.objects.create(ip_address='192.168.1.10', mac_address='AA:BB:CC:DD:EE:01', hostname='WIN-01', location='HQ')
        win2 = WindowsDevice.objects.create(ip_address='192.168.1.11', mac_address='AA:BB:CC:DD:EE:02', hostname='WIN-02', location='Branch')
        WindowsDeviceStatus.objects.create(device=win1, is_online=True)
        WindowsDeviceStatus.objects.create(device=win2, is_online=False)
        print('Windows devices created')
    except Exception as e:
        print('Error creating Windows devices:', e)

    # Android devices
    try:
        and1 = AndroidDevice.objects.create(ip_address='10.0.0.5', mac_address='11:22:33:44:55:01', hostname='AND-01', location='HQ')
        and2 = AndroidDevice.objects.create(ip_address='10.0.0.6', mac_address='11:22:33:44:55:02', hostname='AND-02', location='Remote')
        AndroidDeviceStatus.objects.create(device=and1, is_online=True)
        AndroidDeviceStatus.objects.create(device=and2, is_online=False)
        print('Android devices created')
    except Exception as e:
        print('Error creating Android devices:', e)

    # Print device counts after creation attempts
    print('WindowsDevice count:', WindowsDevice.objects.count())
    print('AndroidDevice count:', AndroidDevice.objects.count())

if __name__ == "__main__":
    # Add project root to sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "device_health.settings")
    django.setup()
    seed()
