# create_admin.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Laundry_p.settings")  # adjust if your settings module is different
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "Admin"
email = "ermiasmaz8069@gmail.com"
password = "12345?"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created.")
else:
    print("⚠️ Superuser already exists.")
