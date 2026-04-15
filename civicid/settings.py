from pathlib import Path
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&856=-$xw=89o7$&&bb^-mo%0)9y3gv0=5cq(+iwc8iar615(9'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    "rest_framework",
    "corsheaders",

    # CivicID apps
    "apps.accounts",
    "apps.persons",
    "apps.person_photos",
    "apps.birth_records",
    "apps.naturalization",
    "apps.immigration_status",
    "apps.id_applications",
    "apps.issued_ids",
    "apps.audit",
    "apps.law_enforcement",
    "apps.voter_registration",
    "apps.passports",
    "apps.death_records",
    "apps.marriage_certificates",
    "apps.social_security",
    "apps.selective_service",
    "apps.civic_tasks",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'civicid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates' / 'civicid-frontend'],
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

WSGI_APPLICATION = 'civicid.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'templates' / 'civicid-frontend' / 'css',
    BASE_DIR / 'templates' / 'civicid-frontend' / 'js',
]

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'   # Changed from templates/media to project root /media/

# ── CELERY ───────────────────────────────────────────────────────
CELERY_BROKER_URL        = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND    = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE          = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'run-daily-civic-checks': {
        'task': 'apps.civic_tasks.tasks.run_daily_civic_checks',
        'schedule': crontab(hour=0, minute=0),   # Every day at midnight UTC
    },
    'deregister-selective-service-age-26': {
        'task': 'apps.civic_tasks.tasks.deregister_selective_service_age_26',
        'schedule': crontab(hour=0, minute=30),  # Daily at 00:30 UTC
    },
}