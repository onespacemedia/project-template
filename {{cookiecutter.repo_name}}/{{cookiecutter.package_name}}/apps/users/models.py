from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        if 'username' in extra_fields:
            del extra_fields['username']

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(
            email,
            password,
            False,
            False,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            True,
            True,
            **extra_fields
        )

    # Make user emails case-insensitive.
    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Standard auth fields not supplied by mixins/base class
    email = models.EmailField(
        "email address",
        max_length=100,
        unique=True,
        error_messages={
            'unique': 'A user with this email address already exists.',
        }
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin '
                  'site.'
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.'
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ' '.join([self.first_name, self.last_name]).strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
