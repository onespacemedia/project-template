# Taken mostly from https://github.com/django/django/blob/11ade8eefd32f5bc7ee6379b77824f02ca61c20b/django/core/serializers/json.py#L76
# Support for encoding model objects has been added.

# Avoid shadowing the standard library json module
from __future__ import absolute_import, unicode_literals

import datetime
import decimal
import json
import uuid

import six
# from django.apps import apps;  apps.get_model
from django.db.models import Model
from django.utils.duration import duration_iso_string
from django.utils.functional import Promise
from django.utils.timezone import is_aware


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types and UUIDs.
    """

    def default(self, o):  # pylint: disable=too-complex,too-many-return-statements,too-many-branches,method-hidden
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        if isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, Promise):
            return six.text_type(o)
        if isinstance(o, Model):
            return {
                'app_label': o._meta.app_label,
                'model_name': o._meta.model_name,
                'pk': o.pk,
            }
        return super(DjangoJSONEncoder, self).default(o)
