from django.core.management import call_command
from django.http import HttpResponse
from django.db import connection


def fix_db(request):
    log = []
    try:
        # 1. Force check the connection
        connection.ensure_connection()
        log.append("Database connection: OK")

        # 2. Run migrations with --fake-initial
        # This fixes 'socialaccount', 'auth', and 'sessions'
        # while ignoring the 'django_site' table we already made.
        call_command('migrate', '--fake-initial', interactive=False)
        log.append("All migrations applied (with --fake-initial): SUCCESS")

        return HttpResponse("<br>".join(log))
    except Exception as e:
        return HttpResponse(f"Error during repair: {str(e)}", status=500)
