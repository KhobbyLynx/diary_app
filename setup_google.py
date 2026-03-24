import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'diaryapp.settings'
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Remove ALL duplicate Google apps
google_apps = SocialApp.objects.filter(provider='google')
count = google_apps.count()
print(f'Found {count} Google SocialApp entries')

if count > 1:
    # Keep only the first one, delete rest
    first = google_apps.first()
    google_apps.exclude(pk=first.pk).delete()
    print(f'Deleted {count - 1} duplicates, kept: {first.name} (id={first.pk})')
elif count == 0:
    # Create one
    app = SocialApp.objects.create(
        provider='google',
        name='Google',
        client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
        secret=os.getenv('GOOGLE_CLIENT_SECRET', ''),
    )
    site = Site.objects.get_current()
    app.sites.add(site)
    print(f'Created new SocialApp: {app.name}')
else:
    first = google_apps.first()
    print(f'Only 1 entry exists: {first.name} (id={first.pk}) - OK')

# Make sure the remaining one is linked to the site
app = SocialApp.objects.get(provider='google')
site = Site.objects.get_current()
app.sites.add(site)
print(f'Linked to site: {site.domain}')
print(f'client_id: {app.client_id[:25]}...')
