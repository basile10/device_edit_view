from django.contrib.auth.models import User
from health.models import UserRole

def check_superadmin_role():
    try:
        user = User.objects.get(username='superadmin')
        print('superadmin user id:', user.id)
        exists = UserRole.objects.filter(user_id=user.id, role='superadmin').exists()
        print('UserRole exists for superadmin:', exists)
        if not exists:
            print('Creating UserRole for superadmin...')
            UserRole.objects.update_or_create(user_id=user.id, defaults={'role': 'superadmin'})
            print('UserRole created.')
        else:
            print('UserRole already exists.')
    except Exception as e:
        print('Error:', e)

check_superadmin_role()
