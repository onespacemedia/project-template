from django.contrib import admin
from social_django.models import Association, Nonce, UserSocialAuth

# Unregister python social auth models (not really needed or useful).
for model in [Association, Nonce, UserSocialAuth]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
