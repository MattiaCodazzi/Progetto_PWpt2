from pathlib import Path
import os, dotenv
import dj_database_url

# --------------------------------------------------
#  BASE PATH & .env
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# Carica variabili d'ambiente da .env (se presente)
dotenv.load_dotenv(BASE_DIR / '.env')

# --------------------------------------------------
#  SECURITY / DEBUG
# --------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'insecure-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# È possibile passare ALLOWED_HOSTS nel .env come lista separata da virgole
ALLOWED_HOSTS = [h for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h] or []

# --------------------------------------------------
#  APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd‑party
    'django_bootstrap5',
    # Local apps
    'gallery',
]

# --------------------------------------------------
#  MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serve i file statici anche in produzione
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------
#  URL & WSGI
# --------------------------------------------------
ROOT_URLCONF = 'museo_site.urls'
WSGI_APPLICATION = 'museo_site.wsgi.application'

# --------------------------------------------------
#  TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'gallery' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------------
#  DATABASE
# --------------------------------------------------
# Usa DJ_DATABASE_URL per switch automatico (PostgreSQL in .env oppure fallback SQLite)
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DB_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
        ssl_require=False,
    )
}

# --------------------------------------------------
#  PASSWORD VALIDATORS (puoi configurarli più avanti)
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# --------------------------------------------------
#  I18N / TIMEZONE
# --------------------------------------------------
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
#  STATIC & MEDIA FILES
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Se prevedi file statici custom (CSS/JS) crea la cartella "static" o commenta la riga sotto
# STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise: abilita compressione e cache‐headers
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------------------------------------
#  DEFAULT PRIMARY KEY & OTHER GLOBALS
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

