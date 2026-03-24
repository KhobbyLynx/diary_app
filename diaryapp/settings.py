"""
Django settings for diaryapp project.
Refactored for Production (Render + PostgreSQL) and Local Development.
Key features:
- Environment variable management with python-dotenv
- Database configuration that auto-switches between PostgreSQL (Render) and SQLite (local)
- Django-Allauth setup for Google OAuth2 authentication
- Whitenoise for static file management in production
- Security settings that adapt based on DEBUG mode
"""

import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# --- ENVIRONMENT VARIABLES ---
# Secret key should be in .env for local, or Environment Variables on Render
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'django-insecure-fallback-for-local-only-s84*8hy23o#5t9+32)#79c8ri8')

# DEBUG is True locally, False in production
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allow hosts for Render/Testing;
ALLOWED_HOSTS = [os.environ.get(
    'RENDER_EXTERNAL_HOSTNAME'), 'localhost', '127.0.0.1']

# Groq API key for LLaMA 3.3 integration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')


# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'whitenoise.runserver_nostatic',  # Manages static files in production

    # Project apps
    'diary',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Essential for Render hosting
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- DJANGO-ALLAUTH SETTINGS ---
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            # 'prompt': 'select_account', # Uncomment this to always force account selection
        },
        'OAUTH_PKCE_ENABLED': True,
        'VERIFIED_EMAIL': True,
    },
}
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

ROOT_URLCONF = 'diaryapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'diaryapp.wsgi.application'


# --- DATABASE CONFIG ---
# Switches between PostgreSQL (Render) and SQLite (Local)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG  # Require SSL only in production
    )
}


# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES ---
STATIC_URL = 'static/'
# Folder where collectstatic will dump files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- EMAIL ---
# Using console backend for simplicity in a test project
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
