from .base import *  # pylint: disable=unused-wildcard-import,wildcard-import

DEBUG = False
TEMPLATE_DEBUG = DEBUG
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'rollbar': {
            'access_token': '{{ cookiecutter.rollbar_access_token }}',
            'environment': 'production',
            'class': 'rollbar.logger.RollbarHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        '{{ cookiecutter.package_name }}': {
            'level': 'WARNING',
            'handlers': ['rollbar'],
            'propagate': False,
        },
    },
}
