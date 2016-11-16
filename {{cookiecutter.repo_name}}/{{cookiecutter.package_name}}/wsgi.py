import os

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.package_name}}.settings.production')

# For HTTPS sites, enable these.
# os.environ.setdefault('HTTPS', 'on')
# os.environ.setdefault('wsgi.url_scheme', 'https')

application = get_wsgi_application()
