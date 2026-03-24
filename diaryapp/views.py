import os
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.http import HttpResponse


def fix_db(request):

    # Inside your fix_db function:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            'admin', 'admin@lynxnet.com', 'Testing@123')

    try:
        # 1. Get the keys you already set in Render Env
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        secret = os.environ.get('GOOGLE_CLIENT_SECRET')

        if not client_id or not secret:
            return HttpResponse("🔴 Error: Missing GOOGLE_CLIENT_ID or SECRET in Render Environment Variables.")

        # 2. Fix the Site record (Required for Social Login)
        site, _ = Site.objects.get_or_create(
            id=1,
            defaults={'domain': 'diary-app-mvp2.onrender.com',
                      'name': 'Diary App'}
        )
        # Force the domain to be correct if it exists but is wrong
        site.domain = 'diary-app-mvp2.onrender.com'
        site.name = 'Diary App'
        site.save()

        # 3. Create the SocialApp record that is currently "DoesNotExist"
        app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google Login',
                'client_id': client_id,
                'secret': secret,
            }
        )

        # If it already existed, update the keys to match the Env
        if not created:
            app.client_id = client_id
            app.secret = secret
            app.save()

        # 4. Link the app to the site (Crucial step!)
        app.sites.add(site)

        return HttpResponse("<h1>✅ Success!</h1> Keys synced to DB. <a href='/accounts/login/'>Click here to Login</a>")
    except Exception as e:
        return HttpResponse(f"🔴 Fix failed: {str(e)}")
