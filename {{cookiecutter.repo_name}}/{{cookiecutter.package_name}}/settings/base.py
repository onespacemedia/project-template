from __future__ import unicode_literals

import os
import platform
import sys

from django_jinja.builtins import DEFAULT_EXTENSIONS
from social_core.pipeline import DEFAULT_AUTH_PIPELINE

if platform.python_implementation() == 'PyPy':
    from psycopg2cffi import compat  # pylint: disable=import-error
    compat.register()


###
#  ___
# | _ ) __ _  ___ ___
# | _ \/ _` |(_-</ -_)
# |___/\__,_|/__/\___|
#
###
SITE_NAME = '{{cookiecutter.project_name}}'
SITE_DOMAIN = '{{cookiecutter.domain_name}}'
PREPEND_WWW = True

ALLOWED_HOSTS = [
    SITE_DOMAIN,
    'www.{}'.format(SITE_DOMAIN),
    'www.{{cookiecutter.staging_subdomain}}.onespace.media',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
    }
}

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
{% if cookiecutter.geoip == 'no' %}# {% endif %}GEOIP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../geoip/'))

CELERY_BROKER_URL = 'redis://localhost:6379/0'

# A secret key used for cryptographic algorithms.
SECRET_KEY = ' '
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Ignores certain warnings on startup and/or `manage.py check`
SILENCED_SYSTEM_CHECKS = []

# Absolute path to the directory where templates are stored.
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            os.path.join(SITE_ROOT, 'assets/svg'),
            os.path.join(SITE_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.html',
            'match_regex': r'^(?!admin/|reversion/|registration/|sitemap\.xml|debug_toolbar/).*',
            'app_dirname': 'templates',
            'newstyle_gettext': True,
            'extensions': DEFAULT_EXTENSIONS + [
                'webpack_loader.contrib.jinja2ext.WebpackExtension',
                'compressor.contrib.jinja2ext.CompressorExtension',
                '{{cookiecutter.package_name}}.apps.site.extensions.DjangoNow',
            ],
            'bytecode_cache': {
                'name': 'default',
                'backend': 'django_jinja.cache.BytecodeCache',
                'enabled': False,
            },
            'autoescape': True,
            'auto_reload': False,
            'translation_engine': 'django.utils.translation',
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'cms.context_processors.settings',
                'cms.apps.pages.context_processors.pages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ]
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'cms.context_processors.settings',
                'cms.apps.pages.context_processors.pages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ]
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


###
#  ___             _           _                         _   __  _
# | _ \ _ _  ___  (_) ___  __ | |_    ___ _ __  ___  __ (_) / _|(_) __
# |  _/| '_|/ _ \ | |/ -_)/ _||  _|  (_-<| '_ \/ -_)/ _|| ||  _|| |/ _|
# |_|  |_|  \___/_/ |\___|\__| \__|  /__/| .__/\___|\__||_||_|  |_|\__|
#               |__/                     |_|
###
NEWS_APPROVAL_SYSTEM = False

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = False
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'flexible_images',
    'sorl.thumbnail',
    'compressor',

    'django_jinja',
    'django_lazy_image',

    'cms',

    'reversion',
    'historylinks',
    'watson',

    'cms.apps.pages',
    'cms.apps.links',
    'cms.apps.media',
    # Needs to be before `apps.site` so that unregistering social auth models
    # in site/admin.py works.
    'social_django',

    {% if cookiecutter.careers == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.careers',
    '{{cookiecutter.package_name}}.apps.components',
    {% if cookiecutter.events == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.events',
    {% if cookiecutter.faqs == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.faqs',
    {% if cookiecutter.news == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.news',
    {% if cookiecutter.partners == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.partners',
    {% if cookiecutter.people == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.people',
    {% if cookiecutter.redirects == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.redirects',
    {% if cookiecutter.sections == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.sections',
    '{{cookiecutter.package_name}}.apps.settings',
    '{{cookiecutter.package_name}}.apps.site',

    'suit',
    'django.contrib.admin',

    'server_management',
    'django_extensions',
    'cachalot',
    'webpack_loader',
]

###
#  ___               _  _                  _
# | __| _ __   __ _ (_)| |  __ _  _ _   __| |  ___  _ _  _ _  ___  _ _  ___
# | _| | '  \ / _` || || | / _` || ' \ / _` | / -_)| '_|| '_|/ _ \| '_|(_-<
# |___||_|_|_|\__,_||_||_| \__,_||_||_|\__,_| \___||_|  |_|  \___/|_|  /__/
#
###
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'developers@onespacemedia.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

SERVER_EMAIL = '{name} <notifications@{domain}>'.format(
    name=SITE_NAME,
    domain=SITE_DOMAIN,
)
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = []
MANAGERS = ()
SEND_BROKEN_LINK_EMAILS = False


###
#  ___   _                  _        _
# |   \ (_) ___ _ __  __ _ | |_  __ | |__
# | |) || |(_-<| '_ \/ _` ||  _|/ _|| '  \
# |___/ |_|/__/| .__/\__,_| \__|\__||_||_|
#              |_|
###
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    {% if cookiecutter.geoip == 'no' %}# {% endif %}'cms.middleware.LocalisationMiddleware',
    {% if cookiecutter.redirects == 'no' %}# {% endif %}'{{cookiecutter.package_name}}.apps.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'watson.middleware.SearchContextMiddleware',
    'historylinks.middleware.HistoryLinkFallbackMiddleware',
    'cms.middleware.PublicationMiddleware',
    'cms.apps.pages.middleware.PageMiddleware',
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


###
#  _____  _     _          _                     _
# |_   _|| |_  (_) _ _  __| |   _ __  __ _  _ _ | |_  _  _
#   | |  | ' \ | || '_|/ _` |  | '_ \/ _` || '_||  _|| || |
#   |_|  |_||_||_||_|  \__,_|  | .__/\__,_||_|   \__| \_, |
#                              |_|                    |__/
###
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend'
)
SUIT_CONFIG = {
    'ADMIN_NAME': SITE_NAME,
    'MENU_EXCLUDE': ['default'],
}
SOCIAL_AUTH_GOOGLE_PLUS_KEY = '{{cookiecutter.google_plus_key}}'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '{{cookiecutter.google_plus_secret}}'
GOOGLE_ANALYTICS = '{{cookiecutter.google_analytics}}'
ADMIN_ANALYTICS_ID = GOOGLE_ANALYTICS
ADMIN_ANALYTICS_GOOGLE_API_KEY = '{{cookiecutter.google_analytics_key}}'

# You can get your Client ID & Secret here: https://creativesdk.adobe.com/myapps.html
ADOBE_CREATIVE_SDK_ENABLED = {% if cookiecutter.adobe_creative_sdk_secret and cookiecutter.adobe_creative_sdk_id %}True{% else %}False{% endif %}
ADOBE_CREATIVE_SDK_CLIENT_SECRET = '{{cookiecutter.adobe_creative_sdk_secret}}'
ADOBE_CREATIVE_SDK_CLIENT_ID = '{{cookiecutter.adobe_creative_sdk_id}}'

WHITELISTED_DOMAINS = ['onespacemedia.com']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/admin/'
SOCIAL_AUTH_PIPELINE = DEFAULT_AUTH_PIPELINE + (
    'cms.pipeline.make_staff',
)

TINYPNG_API_KEY = '{{cookiecutter.tinypng_api_key}}'

TYPEKIT_KIT_ID = '{{cookiecutter.typekit_kit_id}}'
GOOGLE_FONTS_KIT_URL = '{{cookiecutter.google_fonts_kit_url}}'

ROLLBAR_SERVER_TOKEN = '{{ cookiecutter.rollbar_server_token }}'
ROLLBAR_CLIENT_TOKEN = '{{ cookiecutter.rollbar_client_token }}'

WYSIWYG_OPTIONS = {
    # Overall height of the WYSIWYG
    'height': 500,

    # Main plugins to load, this has been stripped to match the toolbar
    # See https://www.tinymce.com/docs/get-started/work-with-plugins/
    'plugins': [
        'advlist autolink link image lists charmap hr anchor pagebreak',
        'wordcount visualblocks visualchars code fullscreen cmsimage hr template',
        'table contextmenu directionality paste textcolor colorpicker textpattern'
    ],

    # Items to display on the 3 toolbar lines
    'toolbar1': 'code | cut copy paste pastetext | undo redo | bullist numlist | link unlink anchor cmsimage | blockquote charmap',
    'toolbar2': 'template styleselect formatselect | bold italic underline hr | alignleft aligncenter alignright | table | removeformat | subscript superscript',
    'toolbar3': '',

    # Display menubar with dropdowns
    'menubar': False,

    # Make toolbar smaller
    'toolbar_items_size': 'small',

    # These come from assets/html and are moved into these file paths by Gulp
    'templates': [
        {
            'title': 'Test',
            'description': 'A test template',
            'url': '/static/build/html/test.html'
        }
    ],

    'block_formats': 'Paragraph=p;Header 2=h2;Header 3=h3;Header 4=h4;Header 5=h5;Header 6=h6;',

    # Custom style formats
    'style_formats': [
        {
            'title': 'Buttons',
            'items': [
                {
                    'title': 'Primary',
                    'selector': 'a',
                    'classes': 'wys-Button-primary'
                },
                {
                    'title': 'Secondary',
                    'selector': 'a',
                    'classes': 'wys-Button-secondary'
                },
            ]
        },
        {
            'title': 'Titles',
            'items': [
                {
                    'title': 'Small',
                    'selector': 'h1,h2,h3,h4,h5,h6',
                    'classes': 'wys-Title-small'
                },
                {
                    'title': 'Medium',
                    'selector': 'h1,h2,h3,h4,h5,h6',
                    'classes': 'wys-Title-medium'
                },
                {
                    'title': 'Large',
                    'selector': 'h1,h2,h3,h4,h5,h6',
                    'classes': 'wys-Title-large'
                },
                {
                    'title': 'Extra large',
                    'selector': 'h1,h2,h3,h4,h5,h6',
                    'classes': 'wys-Title-extraLarge'
                }
            ]
        }
    ],

    # Make all elements valid
    'valid_elements': '*[*]',

    # Disable automatic URL manipulation
    'convert_urls': False,

    # Make TinyMCE past as text by default
    'paste_as_text': True,

    'image_advtab': True,

    # Custom CSS to style the wysiwyg content area
    'content_css': '/static/build/css/wysiwyg.css'
}


###
#  _   _        _                _          _     __      _          _    _
# | | | | _ __ | | ___  __ _  __| | ___  __| |   / /  ___| |_  __ _ | |_ (_) __
# | |_| || '_ \| |/ _ \/ _` |/ _` |/ -_)/ _` |  / /  (_-<|  _|/ _` ||  _|| |/ _|
#  \___/ | .__/|_|\___/\__,_|\__,_|\___|\__,_| /_/   /__/ \__|\__,_| \__||_|\__|
#        |_|
###
MEDIA_ROOT = '/var/www/{{cookiecutter.package_name}}_media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/var/www/{{cookiecutter.package_name}}_static'
STATIC_URL = '/static/'

FILE_UPLOAD_PERMISSIONS = 0o644
NODE_MODULES_ROOT = '/var/www/{{cookiecutter.package_name}}_static'
NODE_MODULES_URL = '/static/'

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
THUMBNAIL_QUALITY = 60


###
#  _  _       _                     _        _     _
# | \| | ___ | |_  __ __ __ _  _ _ (_) __ _ | |__ | | ___  ___
# | .` |/ _ \|  _| \ V // _` || '_|| |/ _` || '_ \| |/ -_)(_-<
# |_|\_|\___/ \__|  \_/ \__,_||_|  |_|\__,_||_.__/|_|\___|/__/
#
###

# Current commit hash, used for cache-busting CSS.
try:
    GIT_COMMIT_HASH = os.popen('git rev-parse --short HEAD').read().strip()
# Catch everything so we don't stop the application starting if there's a problem.
except:  # pylint: disable=bare-except
    GIT_COMMIT_HASH = ''

if 'test' in sys.argv:
    # The CMS tests use test-only models, which won't be loaded if we only load
    # our real migration files, so point to a nonexistent one, which will make
    # the test runner fall back to 'syncdb' behavior.

    # Note: This will not catch a situation where a developer commits model
    # changes without the migration files.

    MIGRATION_MODULES = {}
    for app in INSTALLED_APPS:
        app_name = app.split('.')[-1]
        MIGRATION_MODULES[app_name] = None

    # Remove the localisation middleware
    if 'cms.middleware.LocalisationMiddleware' in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES = tuple(
            c for c in MIDDLEWARE_CLASSES if c != 'cms.middleware.LocalisationMiddleware')
