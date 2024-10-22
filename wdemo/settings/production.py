from .base import *
import os

DEBUG = False  # Set to False for production

# Update ALLOWED_HOSTS to include your Render domain and EC2 IP address
ALLOWED_HOSTS = [
    'icprofsensei-github-io.onrender.com',  # Your Render domain without 'https://'
    '13.48.45.57',                          # Your EC2 public IP
    os.getenv('RENDER_EXTERNAL_HOSTNAME'),   # Optional: can be used for Render's external hostname
]

# Configure static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),                # Your PostgreSQL database name
        'USER': os.environ.get('DB_USER'),                # Your PostgreSQL username
        'PASSWORD': os.environ.get('DB_PASSWORD'),        # Your PostgreSQL password
        'HOST': os.environ.get('DB_HOST', 'localhost'),   # Use 'localhost' if DB is on the same EC2 instance
        'PORT': os.environ.get('DB_PORT', '5432'),        # Default PostgreSQL port
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Backend URL for API requests
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

# Security settings for HTTPS
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
SESSION_COOKIE_SECURE = True  # Ensures cookies are only sent over HTTPS
CSRF_COOKIE_SECURE = True 
