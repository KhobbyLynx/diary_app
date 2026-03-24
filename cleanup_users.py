"""Quick cleanup script to fix broken users from failed signups."""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diaryapp.settings')
django.setup()

from django.contrib.auth.models import User

# Find and delete users with empty username (created by broken signups)
broken = User.objects.filter(username='')
count = broken.count()
if count:
    broken.delete()
    print(f"Deleted {count} broken user(s) with empty username.")
else:
    print("No broken users found.")

# Show all users
users = User.objects.all()
print(f"\nTotal users in database: {users.count()}")
for u in users:
    print(f"  - id={u.id}, username='{u.username}', email='{u.email}'")
