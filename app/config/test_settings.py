from app.config.base_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME_TEST', 'postgres'),
            'USER': os.environ.get('DATABASE_USER_TEST', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD_TEST', 'root'),
        'HOST': os.environ.get('DATABASE_HOST_TEST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT_TEST', '5432'),
        'CONN_MAX_AGE': 600,
    }
}