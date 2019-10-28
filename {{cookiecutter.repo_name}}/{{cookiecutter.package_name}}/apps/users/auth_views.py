"""Views used by the CMS news app."""
from django.contrib.auth.views import password_reset_confirm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView

from .forms import PasswordResetForm, SetPasswordForm


class PasswordResetView(FormView):
    form_class = PasswordResetForm

    template_name = 'users/reset/password_reset_form.html'

    success_url = reverse_lazy('password_reset_sent')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(domain_override='ignore')
        return super().form_valid(form)


class PasswordResetSentView(TemplateView):
    template_name = 'users/reset/password_reset_sent.html'


class PasswordResetConfirmView(View):
    def dispatch(self, request, *args, **kwargs):
        return password_reset_confirm(
            request,
            uidb64=kwargs['uidb64'],
            token=kwargs['token'],
            post_reset_redirect=u'{}?reset_successful=1'.format(reverse_lazy('admin:login')),
            template_name='users/reset/password_reset_confirm.html',
            set_password_form=SetPasswordForm,
        )
