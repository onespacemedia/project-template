from django.apps import AppConfig
from django.contrib import admin


class SiteAppConfig(AppConfig):
    name = '{{cookiecutter.package_name}}.apps.site'

    def ready(self):
        # Unregister python social auth models (not really needed or useful).
        #
        # Import needs to be here as it won't work at the top level of the
        # file.
        from social_django.models import Association, Nonce, UserSocialAuth

        for model in [Association, Nonce, UserSocialAuth]:
            try:
                admin.site.unregister(model)
            except admin.sites.NotRegistered:
                pass
