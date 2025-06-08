# create_admin.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Laundry_p.settings')  # Replace with your project name
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'ermiasmaz8069@gmail.com', 'Admin')
    print("Superuser created.")
else:
    print("Superuser already exists.")
