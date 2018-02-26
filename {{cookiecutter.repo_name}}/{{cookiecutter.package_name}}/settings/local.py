import os
import os.path

from .base import *  # pylint: disable=unused-wildcard-import,wildcard-import

# Run in debug mode.
DEBUG = True

# Save media files to the user's Sites folder.
MEDIA_ROOT = os.path.expanduser(os.path.join('~/Sites', SITE_DOMAIN, 'media'))
STATIC_ROOT = os.path.expanduser(os.path.join('~/Sites', SITE_DOMAIN, 'static'))
NODE_MODULES_ROOT = os.path.expanduser(os.path.join('~/Workspace/{{cookiecutter.package_name}}', 'node_modules'))


# Use local server.

SITE_DOMAIN = 'localhost:8000'

ALLOWED_HOSTS = [
    # Django's defaults.
    '127.0.0.1',
    'localhost',
    '::1',
    # For compatibility with Browsersync.
    '0.0.0.0',
]

PREPEND_WWW = False

# Optional separate database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
    },
}

# Mailtrip SMTP
EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = '178288370161874a6'
EMAIL_HOST_PASSWORD = '5033a6d5bca3f0'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
