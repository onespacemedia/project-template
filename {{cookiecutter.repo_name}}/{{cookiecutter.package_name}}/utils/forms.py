from django.core.exceptions import ValidationError

from ..apps.site.models import User


class UserEmailUniqueFormMixin:
    '''
    A mixin for ModelForm derivatives for the User model that want to
    enforce no two users having the same *case-insensitive* email address
    (case-sensitive uniqueness is already enforced). This includes both the
    cases where a user is created, and when a user is changed - it'll allow
    developers@onespacemedia.com to be changed to DEVELOPERS@ONESPACEMEDIA.COM
    but won't allow anyone else to change it to the same.

    This is currently in use in UserCreationForm and
    UserCreationAdminForm in admin.py, but should probably be used for the
    user-facing registration forms above too at some point.
    '''
    def clean_email(self):
        value = self.cleaned_data.get('email')
        if value:
            users = User.objects.filter(email__iexact=value)

            if self.instance and self.instance.pk:
                users = users.exclude(pk=self.instance.pk)

            if users.exists():
                raise ValidationError('A user with that email address already exists.')

        return value
