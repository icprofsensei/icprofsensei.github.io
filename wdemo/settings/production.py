from .base import * 


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.getenv('RENDER_EXTERNAL_HOSTNAME'), '']

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
    'default': dj_database_url.config(
        default = os.environ.get('DATABASE_URL', 'postgresql://testtep_user:wkszhtPHvj7HfwjBZeE26IYcdYgHo0FZ@dpg-csbu6qjtq21c73a8k0ig-a/testtep')
    )
}

'''
'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),     # Replace with the name of your PostgreSQL database
        'USER': os.environ.get('DB_USER'),     # Replace with your PostgreSQL username (e.g., 'postgres')
        'PASSWORD': os.environ.get('DB_PASSWORD'),      # Replace with your PostgreSQL password
        'HOST': os.environ.get('DB_HOST'),              # Database server address (default: localhost)
        'PORT': os.environ.get('DB_PORT', '5432'),                   # Port number (default: 5432)
    }'''

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Backend URL for API requests
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
