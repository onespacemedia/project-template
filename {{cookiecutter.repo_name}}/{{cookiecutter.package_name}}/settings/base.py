from __future__ import unicode_literals

import os
import platform

from social_core.pipeline import DEFAULT_AUTH_PIPELINE

if platform.python_implementation() == 'PyPy':
    from psycopg2cffi import compat
    compat.register()


# The name of this site.  Used for branding in the online admin area.

SITE_NAME = '{{cookiecutter.project_name}}'

SITE_DOMAIN = '{{cookiecutter.domain_name}}'

PREPEND_WWW = True

ALLOWED_HOSTS = [
    SITE_DOMAIN,
    'www.{}'.format(SITE_DOMAIN),
    'www.{{cookiecutter.staging_subdomain}}.onespace.media',
]

SUIT_CONFIG = {
    'ADMIN_NAME': SITE_NAME,
    'MENU_EXCLUDE': ['default'],
}

# Database settings.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
    }
}


# Absolute path to the directory where all uploaded media files are stored.

MEDIA_ROOT = '/var/www/{{cookiecutter.package_name}}_media'

MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0o644


# Absolute path to the directory where static files will be collected.

STATIC_ROOT = '/var/www/{{cookiecutter.package_name}}_static'

STATIC_URL = '/static/'

NODE_MODULES_ROOT = '/var/www/{{cookiecutter.package_name}}_static'

NODE_MODULES_URL = '/static/'


# Email settings.

EMAIL_HOST = 'smtp.mandrillapp.com'

EMAIL_HOST_USER = 'developers@onespacemedia.com'

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 587

EMAIL_USE_TLS = True

SERVER_EMAIL = '{name} <notifications@{domain}>'.format(
    name=SITE_NAME,
    domain=SITE_DOMAIN,
)

DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME


# Error reporting settings.  Use these to set up automatic error notifications.

ADMINS = (
    ('Onespacemedia Errors', 'errors@onespacemedia.com'),
)

MANAGERS = ()

SEND_BROKEN_LINK_EMAILS = False


# Locale settings.

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Auto-discovery of project location.

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


# A list of additional installed applications.

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'compressor',
    'django.contrib.admin',

    'server_management',
    'django_extensions',
    'cachalot',
    'webpack_loader',
    'social_django',

    'django.contrib.sites',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_file',
    'djangocms_link',
    {% if cookiecutter.redirects == 'yes' %}'djangocms_redirect',{% endif %}

    '{{ cookiecutter.package_name }}',
]

# Additional static file locations.

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'assets'),  # For webpack_loader
    os.path.join(SITE_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'build/',
        'STATS_FILE': os.path.join(BASE_ROOT, 'webpack-stats.json')
    }
}

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
]

COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

THUMBNAIL_PRESERVE_FORMAT = True

# Dispatch settings.

MIDDLEWARE_CLASSES = [
    {% if cookiecutter.redirects == 'yes' %}'djangocms_redirect.middleware.RedirectMiddleware',{% endif %}
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.Argon2PasswordHasher',
)


ROOT_URLCONF = '{{cookiecutter.package_name}}.urls'

WSGI_APPLICATION = '{{cookiecutter.package_name}}.wsgi.application'

PUBLICATION_MIDDLEWARE_EXCLUDE_URLS = (
    '^admin/.*',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SITE_ID = 1

# Absolute path to the directory where templates are stored.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        }
    }
]


# Namespace for cache keys, if using a process-shared cache.

CACHE_MIDDLEWARE_KEY_PREFIX = '{{cookiecutter.package_name}}'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# A secret key used for cryptographic algorithms.

SECRET_KEY = ' '
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Current commit hash, used for cache-busting CSS.
try:
    GIT_COMMIT_HASH = os.popen('git rev-parse --short HEAD').read().strip()
# Catch everything so we don't stop the application starting if there's a problem.
except:
    GIT_COMMIT_HASH = ''

GOOGLE_ANALYTICS = '{{cookiecutter.google_analytics}}'
ADMIN_ANALYTICS_ID = GOOGLE_ANALYTICS
ADMIN_ANALYTICS_GOOGLE_API_KEY = '{{cookiecutter.google_analytics_key}}'

TINYPNG_API_KEY = '{{cookiecutter.tinypng_api_key}}'

# Google Apps authentication.
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '{{cookiecutter.google_plus_key}}'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '{{cookiecutter.google_plus_secret}}'

WHITELISTED_DOMAINS = ['onespacemedia.com']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/admin/'
SOCIAL_AUTH_PIPELINE = DEFAULT_AUTH_PIPELINE + (
    '{{cookiecutter.package_name}}.utils.pipeline.make_staff',
)

# Typekit
TYPEKIT_USED = {% if cookiecutter.uses_typekit == 'yes' %}True{% else %}False{% endif %}
TYPEKIT_KIT_ID = '{{cookiecutter.typekit_kit_id}}'

SILENCED_SYSTEM_CHECKS = []

THUMBNAIL_QUALITY = 60

# Celery config
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# CMS config
CMS_LANGUAGES = {
    # Customize this
    1: [
        {
            'public': True,
            'hide_untranslated': False,
            'name': 'en',
            'code': 'en',
            'redirect_on_fallback': True,
        },
    ],
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
}

# XXX: These seem to be similar to ContentBase templates
CMS_TEMPLATES = (
    # Customize this
    ('general.html', 'General template'),
    ('home.html', 'Home template'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)
