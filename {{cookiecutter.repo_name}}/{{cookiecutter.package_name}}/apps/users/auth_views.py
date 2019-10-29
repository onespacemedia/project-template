from django.contrib.auth.views import (PasswordResetView, PasswordResetCompleteView,
                                       PasswordResetConfirmView, PasswordResetDoneView)

from .forms import ProjectPasswordResetForm, ProjectSetPasswordForm


class ProjectPasswordResetView(PasswordResetView):
    form_class = ProjectPasswordResetForm

    template_name = 'users/reset/password_reset_form.html'


class ProjectPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset/password_reset_done.html'


class ProjectPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = ProjectSetPasswordForm

    template_name = 'users/reset/password_reset_confirm.html'


class ProjectPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset/password_reset_complete.html'

