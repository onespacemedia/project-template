from django.conf.urls import url

from . import auth_views

urlpatterns = [
    url(r'^reset-password/$', auth_views.ProjectPasswordResetView.as_view(), name='password_reset'),
    url(r'^reset-password/sent/$', auth_views.ProjectPasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset-password/complete/$', auth_views.ProjectPasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    url(
        r'^reset-password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.ProjectPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
