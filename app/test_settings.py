from app.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'ubuntu'),
        'USER': os.environ.get('DATABASE_USER', 'circle_test'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'root'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'CONN_MAX_AGE': 600,
    }
}