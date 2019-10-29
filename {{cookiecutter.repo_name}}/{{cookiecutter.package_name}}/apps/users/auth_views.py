"""Views used by the CMS news app."""
from django.contrib.auth.views import (PasswordResetView as BasePasswordResetView,
                                       PasswordResetCompleteView as BasePasswordResetCompleteView,
                                       PasswordResetConfirmView as BasePasswordResetConfirmView,
                                       PasswordResetDoneView as BasePasswordResetDoneView)

from .forms import PasswordResetForm, SetPasswordForm


class PasswordResetView(BasePasswordResetView):
    form_class = PasswordResetForm

    template_name = 'users/reset/password_reset_form.html'


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'users/reset/password_reset_done.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm

    template_name = 'users/reset/password_reset_confirm.html'


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = 'users/reset/password_reset_complete.html'
