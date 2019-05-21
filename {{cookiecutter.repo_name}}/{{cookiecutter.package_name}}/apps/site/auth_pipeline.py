def make_staff(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.is_staff = True
        user.is_superuser = True
        user.save()
