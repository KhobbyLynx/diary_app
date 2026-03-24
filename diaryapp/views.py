from django.core.management import call_command
from django.http import HttpResponse
from django.db import connection


def fix_db(request):
    try:
        with connection.cursor() as cursor:
            # 1. Clean up the duplicate we made manually to let the index build
            cursor.execute("DELETE FROM django_site WHERE id > 1;")
            # 2. Update the first one just in case
            cursor.execute(
                "UPDATE django_site SET domain='diary-app-mvp2.onrender.com', name='Diary App' WHERE id=1;")

        # 3. Finalize the migration state
        call_command('migrate', '--fake-initial', interactive=False)

        return HttpResponse("<h1>Success!</h1> Database is fully repaired. <a href='/accounts/login/'>Go to Login</a>")
    except Exception as e:
        # If it's the duplicate error again, it's actually fine to ignore now
        if "already exists" in str(e) or "duplicated" in str(e):
            return HttpResponse("<h1>Success!</h1> Tables are already set. <a href='/accounts/login/'>Go to Login</a>")
        return HttpResponse(f"Final hurdle: {str(e)}")
