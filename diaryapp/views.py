from django.core.management import call_command
from django.http import HttpResponse


def fix_db(request):
    try:
        # This tells Django to run ALL migrations for ALL apps
        call_command('migrate', interactive=False)
        return HttpResponse("All migrations applied successfully! Your database is now ready.")
    except Exception as e:
        return HttpResponse(f"Migration failed: {str(e)}", status=500)
